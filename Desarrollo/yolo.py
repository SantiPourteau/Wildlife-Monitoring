from ultralytics import YOLO
import torch

#download pre-trained model
#download "yolov11n.pt"
model = YOLO("yolo11n.pt") 
results =  model.train(data="data/dataset_rgb/data.yaml", epochs=3)

