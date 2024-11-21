#Train YOLOV11 with HST Images.

from ultralytics import YOLO
import torch
from torchinfo import summary

if __name__ == "__main__":
    # Cargar el modelo YOLOv11n
    model = YOLO("yolo11n.pt")

    #entrenar sobre gpu
    if torch.cuda.is_available():
        print("GPU disponible")
    else:
        print("GPU no disponible")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Entrenar el modelo con los parámetros especificados
    model.train(
    data="data_hst.yaml",  
    batch=16,  
    imgsz=1024,  
    device=device,  
    epochs = 100)

