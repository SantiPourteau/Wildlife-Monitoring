python "yolov5_4canales\train.py" --data "yolov5_4canales\data_4channels_yolo.yaml" --weights "yolov5_4canales\yolov5s.pt" --img 640 --epochs 75
python "yolov5-master\yolov5-master\train.py" --data "yolov5-master\yolov5-master\data_hst.yaml" --weights "yolov5-master\yolov5-master\yolov5s.pt" --img 640 --epochs 75
python "yolov5-master\yolov5-master\train.py" --data "yolov5-master\yolov5-master\data_rgb.yaml" --weights "yolov5-master\yolov5-master\yolov5s.pt" --img 640 --epochs 75
python "Desarrollo\src\train_models\yolov11_hst.py"
python "Desarrollo\src\train_models\yolov11_rgb.py"
# agregar maskrcnn hst y rgb

