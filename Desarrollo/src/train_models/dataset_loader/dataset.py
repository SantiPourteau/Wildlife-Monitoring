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

    def validate_and_correct_boxes(self, boxes):
        """
        Valida que los cuadros delimitadores tengan dimensiones positivas.
        Corrige el orden de las coordenadas si es necesario.
        """
        valid_boxes = []
        for box in boxes:
            x_min, y_min, x_max, y_max = box
            # Asegurar que las coordenadas estén en el orden correcto
            x_min, x_max = min(x_min, x_max), max(x_min, x_max)
            y_min, y_max = min(y_min, y_max), max(y_min, y_max)

            # Filtrar cuadros con dimensiones no válidas
            if (x_max - x_min) > 0 and (y_max - y_min) > 0:
                print('rotoooo\n')
                valid_boxes.append([x_min, y_min, x_max, y_max])

        return torch.tensor(valid_boxes, dtype=torch.float32)
    
    def generate_masks_from_boxes(self, image_shape, boxes):
        """
        Genera máscaras binarias a partir de bounding boxes.
        - image_shape: tupla con el tamaño (alto, ancho) de la imagen.
        - boxes: lista de cuadros delimitadores (x_min, y_min, x_max, y_max).
        """
        masks = []
        for box in boxes:
            x_min, y_min, x_max, y_max = map(int, box)
            mask = np.zeros(image_shape[:2], dtype=np.uint8)
            mask[y_min:y_max, x_min:x_max] = 1  # Rellena la región del bounding box
            masks.append(mask)
        return torch.tensor(masks, dtype=torch.uint8)
    


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
        # boxes = self.validate_and_correct_boxes(boxes)
        boxes = torch.tensor(boxes, dtype=torch.float32)

        # Generar máscaras sintéticas
        masks = self.generate_masks_from_boxes(image.shape[1:], boxes)

        # Crear el diccionario de etiquetas
        target = {
            "boxes": boxes,
            "labels": torch.tensor(classes, dtype=torch.int64),
            "masks": masks,
        }

        return image, target
