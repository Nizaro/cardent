from ultralytics import YOLO
import torch
import os



def recup_effectif_label(label_path, effectif_cabossage, effectif_rayure, effectif_dechirure, effectif_fissure, effectif_phare_abime):
    dossier_label = os.listdir(label_path)
    i =0
    trouve_cabossage = False
    trouve_rayure = False
    trouve_dechirure = False
    trouve_fissure = False
    trouve_phare_abime = False
    for label in dossier_label:
        #print(label, " : ", "ligne10")
        chemin_label = os.path.join(label_path, label)
        file_name = label.split(".")
        
        fichier = open(chemin_label, "r")
        nb_lignes = len(fichier.readlines())
        
        fichier.seek(0)
        trouve_cabossage = False
        trouve_rayure = False
        trouve_dechirure = False
        trouve_fissure = False
        trouve_phare_abime = False
        
        for ligne in fichier:
            classe = ligne[0]
        
            if(classe == "0") & (trouve_cabossage == False):
                effectif_cabossage += 1
                print("Effectif cabossage: ", effectif_cabossage)
                trouve_cabossage = True
            if(classe == "1") & (trouve_dechirure == False):
                effectif_dechirure += 1
                print("Effectif dechirure: ", effectif_dechirure)
                trouve_dechirure = True
            if(classe == "2") & (trouve_fissure == False):
                effectif_fissure += 1
                print("Effectif fissure: ", effectif_fissure)
                trouve_fissure = True
            if(classe == "3") & (trouve_phare_abime == False):
                effectif_phare_abime += 1
                print("Effectif phare abime: ", effectif_phare_abime)
                trouve_phare_abime= True
            if(classe == "4")& (trouve_rayure == False):
                effectif_rayure += 1
                print("Effectif rayure: ", effectif_rayure)
                trouve_rayure = True
        
    return effectif_cabossage, effectif_rayure, effectif_dechirure, effectif_fissure, effectif_phare_abime

if __name__ == "__main__":
    print(os.getcwd())
    #file = open("test\\labels\\20190119_122723_resized_jpg.rf.6a98209c5edc3c5181da1998bc254c8b.txt","r")
    #classe = file.readline()[0]
    #print(classe)
    effectif_cabossage = 0
    effectif_rayure = 0
    effectif_dechirure = 0
    effectif_fissure = 0
    effectif_phare_abime = 0
    label_path = os.path.join("test\\labels")
    #print(label_path)
    
    effectif_cabossage, effectif_rayure, effectif_dechirure, effectif_fissure, effectif_phare_abime = recup_effectif_label(label_path, effectif_cabossage, effectif_rayure, effectif_dechirure, effectif_fissure, effectif_phare_abime)
    print("Effectif cabossage: ", effectif_cabossage)
    print("Effectif rayure: ", effectif_rayure)
    print("Effectif dechirure: ", effectif_dechirure)
    print("Effectif fissure: ", effectif_fissure)
    print("Effectif phare abime: ", effectif_phare_abime)
    

