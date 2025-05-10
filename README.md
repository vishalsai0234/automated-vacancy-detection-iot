# 📍 Automated Vacancy Detection from Image using IoT Technology

**Real-Time Seat Monitoring with Image Processing, YOLOv5, HTTP, Flask, and ESP32 M5Stack**

---

## 🧠 Project By

Chekuri Muni Siva Keerthan, Ujwal Fandulal Kirsan, Vishal, Yoga Venkata Sai Charan Boddapati  
**Under the guidance of:** Prof. Ratnajeet Bhattacharya & Prof. Arghadip Roy

---

## 📝 Description

This project provides a lightweight, real-time system to automatically detect and display seat vacancy in lecture halls using computer vision and IoT. It integrates **YOLOv5** object detection, a **Flask** backend server, **HTTP communication**, and a **MicroPython-based ESP32 M5Stack** to create a scalable and responsive smart campus tool.

---

## 🚀 Features

- Real-time seat detection from camera images
- YOLOv5-based object detection of empty vs. occupied seats
- ESP32 M5Stack device for capturing images and displaying results
- Flask server for model inference and response
- HTTP-based communication for simplicity and speed
- Easy deployment using low-cost hardware

---

## 🏗️ System Architecture

1. **User Interface**: Triggers seat check  
2. **ESP32 M5Stack**: Captures image, sends via HTTP  
3. **Flask Server**: Receives image, runs YOLOv5 inference  
4. **Result Display**: ESP32 and Web UI show real-time vacancy data  


---

## ⚙️ Methodology

1. **Request Trigger**: UI initiates vacancy check  
2. **Image Capture**: ESP32 captures lecture hall image  
3. **HTTP Upload**: Image sent to Flask server  
4. **Inference**: YOLOv5 detects occupied and vacant seats  
5. **Display Update**: Result displayed on ESP32 and web dashboard  

---

## 🖼️ Dashboard Example

- **Total Seats**: 24  
- **Occupied**: 16  
- **Vacant**: 8  

ESP32 display shows live seat availability using MicroPython graphics.

---

## 📈 Results & Observations

| Metric             | Observation                          |
|--------------------|--------------------------------------|
| Accuracy           | ~90% in well-lit, top-down settings |
| Inference Time     | ~250ms (on server GPU)              |
| System Latency     | ~700ms to 1s overall                |
| Environmental Notes| Performs best in static, bright environments |

---

## 🔮 Applications & Future Work

### 📌 Applications
- Smart classroom scheduling
- Lecture hall seat availability
- Real-time room monitoring
- Event seat tracking

### 📈 Future Enhancements
- ESP32-CAM native integration  
- Cloud dashboard for admins  
- Integration with university timetables  
- Edge deployment with YOLOv5-Tiny  
- Historical data analytics  

---

## 📦 Tech Stack

- **Object Detection**: YOLOv5  
- **Server**: Python + Flask  
- **Device**: ESP32 M5Stack (MicroPython)  
- **Communication**: HTTP  
- **Annotation**: LabelImg with YOLO format

---

## 🛠️ Installation & Setup

### 🔧 Flask Server
```bash
git clone https://github.com/<your-username>/automated-vacancy-detection-iot
cd flask_server/
pip install -r requirements.txt
python app.py
