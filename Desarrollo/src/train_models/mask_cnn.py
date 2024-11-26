import torch
import torchvision
from torchvision.models.detection import MaskRCNN
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone

# Cargar el modelo base
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

# Número de clases (incluye la clase fondo)
num_classes = 3   # 3 clases más la clase fondo

# Cambiar la capa de clasificación (box_predictor)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(
    in_features, num_classes
)

# Cambiar la capa de máscaras (mask_predictor), si aplica
in_channels_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
hidden_layer = 256  # Número de filtros en la capa oculta
model.roi_heads.mask_predictor = torchvision.models.detection.mask_rcnn.MaskRCNNPredictor(
    in_channels_mask, hidden_layer, num_classes
)


#guardar el modelo
torch.save(model.state_dict(), "mask_rcnn_custom.pt")
print("Modelo guardado con éxito!")

