import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import os

#ce fichier permet de visualiser les images inférées et de les réannoter avec nos classes binaires dégat présent ou non
class ImageAnnotator:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Annotator")

        self.image_index = 0
        self.image_list = []
        self.annotations_dir = ""
        self.annotations = []
        self.result_annotations_dir = ""

        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.navigation_frame = tk.Frame(self.master)
        self.navigation_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.prev_button = tk.Button(self.navigation_frame, text="Précédent", command=self.show_prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(self.navigation_frame, text="Suivant", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.damage_var = tk.IntVar()
        self.damage_check = tk.Checkbutton(self.navigation_frame, text="Dégât présent", variable=self.damage_var)
        self.damage_check.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_images_and_annotations()

    def load_images_and_annotations(self):
       
        image_directory = filedialog.askdirectory(title="Select Image Directory")
        if not image_directory:
            return

        
        self.annotations_dir = filedialog.askdirectory(title="Select Annotations Directory")
        if not self.annotations_dir:
            return

        
        self.result_annotations_dir = os.path.join(os.path.dirname(self.annotations_dir), "annotation_result")
        if not os.path.exists(self.result_annotations_dir):
            os.makedirs(self.result_annotations_dir)

        self.image_list = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.image_list.sort()  
        self.image_index = 0
        self.show_image()

    def show_image(self):
        if not self.image_list:
            return

        image_path = self.image_list[self.image_index]
        image = Image.open(image_path)
        #print(f"Image path: {image_path}")

        
        base_name = os.path.basename(image_path)
        annotation_filename = f"{os.path.splitext(base_name)[0]}.txt"  
        annotation_path = os.path.join(self.annotations_dir, annotation_filename)
        #print(f"Opening annotation file: {annotation_path}")

        self.annotations = []

        if os.path.exists(annotation_path):
            #print(f"Annotation file exists: {annotation_path}")
            with open(annotation_path, "r") as file:
                lines = file.readlines()
                if lines:
                    try:
                        self.annotations = [list(map(float, line.strip().split())) for line in lines]
                        #print(f"Loaded annotations: {self.annotations}")
                    except Exception as e:
                        print(f"Error processing annotations: {e}")
                else:
                    print("Annotation file is empty.")
        else:
            print(f"Annotation file does not exist: {annotation_path}")

        
        #print(f"Files in annotations directory: {os.listdir(self.annotations_dir)}")

        self.draw_annotations(image)
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

    def draw_annotations(self, image):
        draw = ImageDraw.Draw(image)
        width, height = image.size

        #print(f"Image dimensions: width={width}, height={height}")

        for annotation in self.annotations:
            class_id, x_center, y_center, w, h = annotation
            left = (x_center - w / 2) * width
            top = (y_center - h / 2) * height
            right = (x_center + w / 2) * width
            bottom = (y_center + h / 2) * height

          
            draw.rectangle([left, top, right, bottom], outline="red", width=2)

    def show_next_image(self):
        self.save_annotation()
        if self.image_index < len(self.image_list) - 1:
            self.image_index += 1
            self.show_image()

    def show_prev_image(self):
        self.save_annotation()
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()

    def save_annotation(self):
        if not self.image_list:
            return

        image_path = self.image_list[self.image_index]
        base_name = os.path.basename(image_path)
        annotation_filename = f"{os.path.splitext(base_name)[0]}.txt" 
        annotation_path = os.path.join(self.result_annotations_dir, annotation_filename)

        with open(annotation_path, "w") as file:
            damage = self.damage_var.get()
            for annotation in self.annotations:
                _, x_center, y_center, w, h = annotation  
                new_class_id = 1 if damage == 1 else 0
                file.write(f"{new_class_id} {x_center} {y_center} {w} {h}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()
