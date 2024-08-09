from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
import torchvision.transforms.functional as F
import os
from torchvision import utils as vutils
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class CustomDataset(Dataset):
    def __init__(self, image_dir, label_dir, transform=None):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.transform = transform
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_name = os.path.join(self.image_dir, self.images[idx])
        label_name = os.path.join(self.label_dir, self.images[idx].replace('.JPG', '.txt').replace('.jpg', '.txt'))
        image = Image.open(img_name).convert("RGB")
        
        # Lire le contenu du fichier .txt
        with open(label_name, 'r') as f:
            label = f.read()
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# Définir les transformations
transformations = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.5),
    transforms.ToTensor()
])

# Créer une instance de votre jeu de données
dataset = CustomDataset(image_dir="Images", label_dir="Labels", transform=transformations)

# Créer un DataLoader pour itérer sur les données
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    
for i, (images, labels) in enumerate(dataloader):
    # Convert the tensor image to a PIL Image for each image in the batch
    for j, image in enumerate(images):
        pil_image = F.to_pil_image(image)
        draw = ImageDraw.Draw(pil_image)
        
        
        
        
       
        # Save the image with the label drawn on it
        pil_image.save(f"augmented_images_{i}_{j}.png")
    
    



