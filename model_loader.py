import torch
from models.experimental import attempt_load

def load_yolov5_model(weights_path=r'utils\best.pt'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = attempt_load(weights_path, map_location=device)
    model.eval()
    return model, device
