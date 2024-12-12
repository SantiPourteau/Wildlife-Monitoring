from ultralytics.models.yolo.detect import DetectionTrainer
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()  # Opcional si no estás generando un ejecutable
    
    args = dict(model="yolo11n.pt", data="data_4channels_yolo.yaml", epochs=75)
    
    # Instancia del entrenador
    trainer = DetectionTrainer(overrides=args)
    
    # Entrenamiento
    trainer.train()
