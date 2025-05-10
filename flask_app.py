import os
import uuid
import requests
from flask import Flask, render_template, request, url_for, jsonify
from PIL import Image
import torch
import numpy as np
import cv2
from threading import Thread
import time

from model_loader import load_yolov5_model
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/uploads')
app.config['RESULT_FOLDER'] = os.path.abspath('static/results')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Load YOLO model
model, device = load_yolov5_model('utils/best.pt')
imgsz = 640

# Cleanup thread
def cleanup_files():
    while True:
        now = time.time()
        for folder in [app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER']]:
            for f in os.listdir(folder):
                path = os.path.join(folder, f)
                if os.path.exists(path) and os.stat(path).st_mtime < now - 86400:
                    try:
                        os.remove(path)
                    except:
                        pass
        time.sleep(3600)

Thread(target=cleanup_files, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image part", 400

    file = request.files['image']
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.jpg")
    file.save(input_path)

    result_path, people_count = process_image(input_path, unique_id)

    # Save last uploaded paths and count
    with open("latest_result.txt", "w") as f:
        f.write(f"{unique_id},{people_count}")

    return "Image received and processed", 200


@app.route('/latest_result')
def latest_result():
    try:
        with open("latest_result.txt", "r") as f:
            line = f.read().strip()
            unique_id, people_count = line.split(",")
        
        input_url = url_for('static', filename=f'uploads/{unique_id}.jpg')
        result_url = url_for('static', filename=f'results/{unique_id}.jpg')

        return render_template("result.html", input_url=input_url, result_url=result_url, people_count=int(people_count))
    except Exception as e:
        return f"No result found. Error: {e}", 404




@app.route('/request_image', methods=['POST'])
def request_image():
    esp32_ip = request.form.get('esp32_ip')  # e.g. 192.168.1.104
    try:
        response = requests.get(f"http://{esp32_ip}/capture", timeout=10)
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Image request sent to ESP32"})
        else:
            return jsonify({"status": "error", "message": f"ESP32 returned {response.status_code}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def process_image(img_path, unique_id):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((imgsz, imgsz))
    img_tensor = torch.from_numpy(np.array(img)).float().permute(2,0,1).unsqueeze(0) / 255.0
    img_tensor = img_tensor.to(device)

    with torch.no_grad():
        pred = model(img_tensor, augment=False)[0]
    pred = non_max_suppression(pred, 0.25, 0.45)[0]

    if pred is not None and len(pred):
        pred[:, :4] = scale_coords(img_tensor.shape[2:], pred[:, :4], img.size).round()

    people_count = len(pred)

    img_np = np.array(img)
    for *xyxy, conf, cls in pred:
        plot_one_box(xyxy, img_np, color=(255, 0, 0), line_thickness=2)

    cv2.putText(img_np, f'People Count: {people_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    result_path = os.path.join(app.config['RESULT_FOLDER'], f"{unique_id}.jpg")
    Image.fromarray(img_np).save(result_path)
    return result_path, people_count

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
