import os
import cv2

# Dossier contenant les images
image_dir = "test/images"
# Dossier contenant les annotations
label_dir = "test/labels"
# Dossier où les images annotées seront sauvegardées
output_dir = "annotated_images"

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

# Mapping des classes
class_mapping = {
    "0": "Cabossage",
    "1": "Dechirure",
    "2": "Fissure",
    "3": "Phare abime",
    "4": "Rayure",
}

# Couleurs pour chaque classe (vous pouvez en ajouter si nécessaire)
colors = {
    "0": (255, 0, 0),   # Cabossage
    "1": (0, 255, 0),   # Dechirure
    "2": (0, 0, 255),   # Fissure
    "3": (255, 255, 0), # Phare abime
    "4": (0, 255, 255), # Rayure
}

for image_file in os.listdir(image_dir):
    if image_file.endswith('.jpg'):
        image_path = os.path.join(image_dir, image_file)
        label_path = os.path.join(label_dir, image_file.replace('.jpg', '.txt'))

        # Lire l'image
        image = cv2.imread(image_path)
        # Faire une copie de l'image pour l'annotation
        annotated_image = image.copy()

        # Vérifier si le fichier de label existe
        if os.path.exists(label_path):
            with open(label_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    class_id = parts[0]
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    # Calculer les coordonnées de la boîte englobante
                    img_height, img_width, _ = image.shape
                    x_min = int((x_center - width / 2) * img_width)
                    y_min = int((y_center - height / 2) * img_height)
                    x_max = int((x_center + width / 2) * img_width)
                    y_max = int((y_center + height / 2) * img_height)

                    # Dessiner la boîte englobante sur l'image annotée
                    color = colors.get(class_id, (255, 255, 255)) # Couleur par défaut blanche
                    cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), color, 2)
                    cv2.putText(annotated_image, class_mapping[class_id], (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Sauvegarder l'image annotée
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, annotated_image)

        print(f"Annotated image saved to {output_path}")
