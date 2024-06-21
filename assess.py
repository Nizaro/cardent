
from ultralytics import YOLO
import torch
import os
import cv2

class_mapping = {
    "0": "Cabossage",
    "1": "Dechirure",
    "2": "Fissure",
    "3": "Phare abime",
    "4": "Rayure",
    # ajoutez d'autres mappages ici si nécessaire
}
#FLAG pour choisir si je fais une prédiction ou pas
PREDICT = False

model = YOLO("runs\\detect\\train2\\weights\\best.pt")
# View all settings
print(model.info())
# Définir le périphérique à utiliser (CPU ou GPU)
class_observed = []
class_to_observe = []
precision_fissure = 0
precision_cabossage = 0
precision_rayure = 0
precision_dechirure = 0
precision_phare_abime = 0

label_path = os.path.join("test\\labels")
      
for fichier in os.listdir("test\\images"):
    if fichier.endswith('.jpg'):
        image_path = os.path.join("test\\images", fichier)
        
        #print(f"Processing image: {image_path}")
        if PREDICT:            
            results = model.predict(image_path,show=True,save_txt=True,show_boxes=True,save=True,)
            annotated_image_path = os.path.join("runs\\detect\\predict", fichier)
            
        '''
            for result in results:
                print(result)
                annotated_image = result.plot()
                
                class_observed = open(label_path, "r").readlines()
                
                class_to_observe = open(label_path, "r").readlines()
                #if(class_observed == class_to_observe):  
                cv2.imwrite(annotated_image_path, annotated_image)
                cv2.imshow("Annotated Image", annotated_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                '''



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
                classes_infered.add(classe)

            for classe in classes_observees:
                if classe in classes_infered:
                    precision_classes[classe] += 1

            fichier_infered.close()

    precision = {class_mapping[k]: (precision_classes[k] / effectif_classes[k]) if effectif_classes[k] > 0 else 0
                 for k in effectif_classes}
    return precision

if __name__ == "__main__":
    label_infered_path = os.path.join("runs\\detect\\predict5\\labels")
    label_path = os.path.join("test\\labels")

    precision = recup_effectif_label(label_path, label_infered_path)

    for classe, value in precision.items():
        print(f"Précision {classe}: {value:.2f}")
