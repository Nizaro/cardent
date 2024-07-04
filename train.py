from ultralytics import YOLO
import torch

if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)

    # Charger le modèle YOLOv8
    model = YOLO("yolov8s.pt")
    print(model.info())
    
    for name, param in model.named_parameters():
     if 'backbone' in name:
        param.requires_grad = False



    # Entraîner le modèle
    result = model.train(data="data.yaml", epochs=200, device=device)

    print(result)
    
    
      