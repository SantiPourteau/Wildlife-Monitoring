import os
import torch
from torch.utils.data import Dataset
import glob
import cv2
import numpy as np


class DatasetConfig:

    def __init__(self, 
                 img_width, img_height, 
                 dataset_path, 
                 splits):
        self.img_width = img_width
        self.img_height = img_height
        self.dataset_path = dataset_path
        self.splits = {}

        for split in splits:
            self.add_split(split)

    def add_split(self, split):
        self.splits[split] = {
            "images": os.path.join(self.dataset_path, split, "images", "*.jpg"),
            "labels": os.path.join(self.dataset_path, split, "labels", "*.txt"),
        }


class ObjectDetectionDataset(Dataset):
    def __init__(self, config, split, is_train=False):
        self.config = config
        self.split = split
        self.is_train = is_train

        # Buscar archivos de imágenes y etiquetas
        self.files = self.find_files()

    def find_files(self):
        splits = self.config.splits
        split = self.split
        return {
            k: sorted(glob.glob(v))
            for k, v in splits[split].items()
        }

    def __len__(self):
        return len(self.files["images"])
    
    def __getitem__(self, index):
        # Leer la imagen y las etiquetas como antes
        image_path = self.files["images"][index]
        label_path = self.files["labels"][index]

        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1) / 255.0

        # Leer etiquetas
        with open(label_path, "r") as f:
            labels = f.readlines()

        boxes = []
        classes = []

        for label in labels:
            cls, x_min, y_min, x_max, y_max = map(float, label.strip().split())
            boxes.append([x_min, y_min, x_max, y_max])
            classes.append(int(cls))

        # Validar y corregir cuadros delimitadores
        boxes = torch.tensor(boxes, dtype=torch.float32)


        # Crear el diccionario de etiquetas
        target = {
            "boxes": boxes,
            "labels": torch.tensor(classes, dtype=torch.int64),
        }

        return image, target
