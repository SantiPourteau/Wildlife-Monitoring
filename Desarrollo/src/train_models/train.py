import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.models.detection.mask_rcnn import MaskRCNN_ResNet50_FPN_Weights
from dataset_loader.dataset import DatasetConfig, ObjectDetectionDataset  # Asegúrate de que estén en el mismo directorio o en el PATH
from torchvision.ops import box_iou

# Configuración del dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando {device}")

# Configuración del Dataset
dataset_config = DatasetConfig(
    img_width=1792, 
    img_height=1434,
    dataset_path="../../data_maskrcnn/dataset_hst",  # Cambia esta ruta por la de tu dataset
    splits=["train_data", "val_data"]
)

# Crear DataLoaders para entrenamiento y validación
train_dataset = ObjectDetectionDataset(config=dataset_config, split="train_data", is_train=True)
val_dataset = ObjectDetectionDataset(config=dataset_config, split="val_data", is_train=False)

# DataLoaders
train_loader = DataLoader(
    train_dataset, 
    batch_size=4, 
    shuffle=True, 
    collate_fn=lambda x: tuple(zip(*x))  # Agrupa las imágenes y etiquetas en listas
)

val_loader = DataLoader(
    val_dataset, 
    batch_size=4, 
    shuffle=False, 
    collate_fn=lambda x: tuple(zip(*x))
)

# Cargar modelo Mask R-CNN solo para detección de objetos
weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
model = maskrcnn_resnet50_fpn(weights=weights)
model.roi_heads.mask_predictor = None  # Remover la cabeza de predicción de máscaras

# Número de clases (incluye la clase fondo)
num_classes = 4  # 3 clases más la clase fondo
in_features = model.roi_heads.box_predictor.cls_score.in_features
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

# Cargar pesos personalizados si corresponde
try:
    model.load_state_dict(torch.load("custom_maskrcnn.pt"))
    print("Pesos personalizados cargados con éxito.")
except FileNotFoundError:
    print("No se encontró el archivo de pesos personalizados. Usando pesos preentrenados.")

model.to(device)

# Optimizador y Scheduler
optimizer = optim.SGD(model.parameters(), lr=0.005, momentum=0.9, weight_decay=0.0005)
lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

# Función de evaluación (mAP)
def evaluate_model(model, data_loader):
    model.eval()
    iou_thresholds = torch.linspace(0.5, 0.95, steps=10)
    metrics = {"mAP": 0.0, "mAP_50": 0.0}

    with torch.no_grad():
        for images, targets in data_loader:
            images = [img.to(device) for img in images]
            print(len(images))
            outputs = model(images)
            print(outputs)
            for output, target in zip(outputs, targets):
                pred_boxes = output["boxes"].to(device)
                pred_labels = output["labels"].to(device)
                true_boxes = target["boxes"].to(device)
                true_labels = target["labels"].to(device)

                ious = box_iou(pred_boxes, true_boxes)
                metrics["mAP_50"] += (ious > 0.5).float().mean().item()

        metrics["mAP_50"] /= len(data_loader.dataset)
        metrics["mAP"] = metrics["mAP_50"]  # Aquí puedes calcular el mAP para otros IoU si es necesario

    return metrics

# Entrenamiento
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    epoch_loss = 0.0
    print(f"Epoch {epoch + 1}/{num_epochs}")
    for images, targets in train_loader:
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        # Adelanto y cálculo de pérdidas
        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        epoch_loss += losses.item()

        # Backpropagation
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        print(f"Loss: {losses.item()}")

    # Actualización del scheduler
    lr_scheduler.step()

    # Evaluación
    metrics = evaluate_model(model, val_loader)

    print(f"Epoch {epoch + 1}/{num_epochs}")
    print(f"Loss: {epoch_loss:.4f}")
    print(f"Validation mAP@50: {metrics['mAP_50']:.4f}")
    print(f"Validation mAP: {metrics['mAP']:.4f}")

# Guardar el modelo reentrenado
torch.save(model.state_dict(), "retrained_maskrcnn.pt")
print("Modelo guardado en 'retrained_maskrcnn.pt'")
