import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import cv2
import numpy as np
from dataset_loader.dataset import ObjectDetectionDataset, DatasetConfig
seed = 1234
random.seed(seed)
def plot_sample(dataset, index=None):
    """
    Función para visualizar una muestra del dataset.
    Muestra la imagen con los cuadros delimitadores y las máscaras generadas.
    """
    # Elegir un índice aleatorio si no se proporciona uno
    if index is None:
        index = random.randint(0, len(dataset) - 1)

    # Obtener una muestra del dataset
    image, target = dataset[index]
    
    # Convertir la imagen a formato HWC para matplotlib
    image = image.permute(1, 2, 0).numpy()  # Convertir a formato HWC para matplotlib

    boxes = target["boxes"].numpy()
    labels = target["labels"].numpy()
    masks = target["masks"].numpy()

    # Crear una figura con subplots
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Imagen con cuadros delimitadores
    ax[0].imshow(image)
    ax[0].set_title("Bounding Boxes")
    ax[0].axis("off")

    for box, label in zip(boxes, labels):
        #get image size
        img_height, img_width, _ = image.shape
        x_center, y_center, width, height = box
        #desnormalizar

        x_center = x_center * img_width
        y_center = y_center * img_height
        width = width * img_width
        height = height * img_height


        x_min = x_center - width / 2
        y_min = y_center - height / 2

        # Crear un rectángulo
        rect = patches.Rectangle(
            (x_min, y_min),
            width,
            height,
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
        ax[0].add_patch(rect)
        ax[0].text(
            x_min,
            y_min - 5,
            f"Class: {label}",
            color="white",
            fontsize=8,
            bbox=dict(facecolor="red", alpha=0.5),
        )

    # Imagen con máscaras generadas
    combined_mask = np.zeros_like(image[:, :, 0])  # Inicializar la máscara combinada en blanco
    for mask in masks:
        combined_mask = np.maximum(combined_mask, mask[0])  # Combinar todas las máscaras

    ax[1].imshow(image, alpha=0.7)
    ax[1].imshow(combined_mask, cmap="viridis", alpha=0.3)
    ax[1].set_title("Generated Masks")
    ax[1].axis("off")

    plt.tight_layout()
    plt.show()

# Configuración del dataset
config = DatasetConfig(
    img_width=640,
    img_height=480,
    dataset_path="../../data_maskrcnn/dataset_hst",  # Cambiar a la ruta de tu dataset
    splits=["train_data"]
)

# Crear una instancia del dataset
dataset = ObjectDetectionDataset(config, split="train_data")

for _ in range(3):
    # plot_sample(dataset)
    print(dataset.__getitem__(0))
