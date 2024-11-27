import torch
import torchvision
from torchvision.models.detection import MaskRCNN
from torchvision.models.detection.mask_rcnn import MaskRCNN_ResNet50_FPN_Weights

# Cargar el modelo base con pesos preentrenados
weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT  # Usar los pesos preentrenados
model = torchvision.models.detection.maskrcnn_resnet50_fpn(weights=weights)

# Número de clases (incluye la clase fondo)
num_classes = 3  # 3 clases más la clase fondo

# Cambiar la capa de clasificación (box_predictor)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(
    in_features, num_classes
)

# Eliminar la cabeza de máscaras (mask_predictor)
model.roi_heads.mask_predictor = None

# Guardar el modelo
torch.save(model.state_dict(), "custom_maskrcnn.pt")
print("Modelo guardado con éxito!")
