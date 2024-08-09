from ultralytics import YOLO
from ultralytics.models.yolo.detect.val import DetectionValidator
import os
from pathlib import Path

import numpy as np
import torch

from ultralytics.data import build_dataloader, build_yolo_dataset, converter
from ultralytics.engine.validator import BaseValidator
from ultralytics.utils import LOGGER, ops
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.metrics import ConfusionMatrix, DetMetrics, box_iou
from ultralytics.utils.plotting import output_to_target, plot_images


# Définir les classes de l'ensemble de données

class_mapping = {
    "0": "Cabossage",
    "1": "Dechirure",
    "2": "Fissure",
    "3": "Phare abime",
    "4": "Rayure",
    
}
#FLAG pour choisir si je fais une prédiction ou pas
PREDICT = False
model = YOLO("runs\\detect\\train24\\weights\\best.pt")
# View all settings
#print(model.info())
# Définir le périphérique à utiliser (CPU ou GPU)
class_observed = []
class_to_observe = []
precision_fissure = 0
precision_cabossage = 0
precision_rayure = 0
precision_dechirure = 0
precision_phare_abime = 0

label_path = os.path.join("test\\labels")


def recup_effectif_label(label_path, label_infered_path):
    dossier_label = os.listdir(label_path)
    effectif_classes = {str(i): 0 for i in range(len(class_mapping))}
    precision_classes = {str(i): 0 for i in range(len(class_mapping))}

    for label in dossier_label:
        chemin_label = os.path.join(label_path, label)
        fichier = open(chemin_label, "r")
        file_name = label.split(".")[0]

        classes_observees = set()
         
        for ligne in fichier:
            classe = ligne.split()[0]
            classes_observees.add(classe)
        
        for classe in classes_observees:
            effectif_classes[classe] += 1

        fichier.close()
        
        label_infered_file = os.path.join(label_infered_path, label)
        if os.path.exists(label_infered_file):
            fichier_infered = open(label_infered_file, "r")
            classes_infered = set()
            for ligne in fichier_infered:
                classe = ligne.split()[0]
                #if classe=="1":
                    #classe="4"
                classes_infered.add(classe)

            for classe in classes_observees:
                if classe in classes_infered:
                    precision_classes[classe] += 1

            fichier_infered.close()

    precision = {class_mapping[k]: (precision_classes[k] / effectif_classes[k]) if effectif_classes[k] > 0 else 0
                 for k in effectif_classes}
    return precision










class CustomDetectionValidator(DetectionValidator):
 def __init__(self, dataloader=None, save_dir=None, pbar=None, args=None, _callbacks=None):
        """Initialize detection model with necessary variables and settings."""
        super().__init__(dataloader, save_dir, pbar, args, _callbacks)
        self.nt_per_class = None
        self.nt_per_image = None
        self.is_coco = False
        self.is_lvis = False
        self.class_map = None
        self.args.task = "detect"
        self.metrics = DetMetrics(save_dir=self.save_dir, on_plot=self.on_plot)
        self.iouv = torch.linspace(0.5, 0.95, 10)  # IoU vector for mAP@0.5:0.95
        self.niou = self.iouv.numel()
        self.lb = []  # for autolabelling

        def assess_batch(self, batch, pred):
            
            
            precision = recup_effectif_label(batch["im_file"], "valid\\labels")
            
            
        
            


validator = CustomDetectionValidator()
    
        
        

metrics_list = []  # Liste pour stocker les métriques de chaque modèle


def main():
    # Load a model
    #model = YOLO("yolov8n.pt")  # load an official model
    for i in range(29, 99):  # Boucle de 1 à 10
        model_path = f"runs\\detect\\train1809\\weights\\epoch{i}.pt"  # Formatage du chemin du modèle
        model = YOLO(model_path)  # Chargement du modèle
        metrics = model.val(plots=False, save_txt=True, conf=0.2)  # Calcul des métriques
    metrics_list.append(metrics)  # Ajout des métriques à la liste

# À ce stade, `metrics_list` contient les métriques pour chaque modèle
    
    

if __name__ == '__main__':
    main()
