
from ultralytics import YOLO
import torch
import os
class_mapping = {
    "0": "Cabossage",
    "1": "Dechirure",
    "2": "Fissure",
    "3": "Phare abime",
    "4": "Rayure",
}

PREDICT = True

model = YOLO("runs\\detect\\train24\\weights\\best.pt")

model.predict("test_fiss.jpeg", show=True, save_txt=True, show_boxes=True, save=True)

# View all settings
print(model.info())
