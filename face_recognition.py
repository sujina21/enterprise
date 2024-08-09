# face_recognition.py
import cv2
import os
import numpy as np
from PIL import Image

def train_face_recognizer(dataset_path):
    if not hasattr(cv2, 'face'):
        raise Exception("OpenCV is not compiled with face module")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def get_images_with_ids(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
        faces = []
        ids = []

        for image_path in image_paths:
            try:
                face_img = Image.open(image_path).convert("L")
                face_np = np.array(face_img, np.uint8)
                id = int(os.path.split(image_path)[-1].split(".")[1])
                print(f"Processing image for ID: {id}")
                faces.append(face_np)
                ids.append(id)
                cv2.waitKey(10)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

        return np.array(ids), faces
    
    try:
        ids, faces = get_images_with_ids(dataset_path)
        recognizer.train(faces, ids)
        os.makedirs("recognizer", exist_ok=True)
        recognizer.save("recognizer/trainingdata.yml")
        print("Training completed and data saved to 'recognizer/trainingdata.yml'")
    except Exception as e:
        print(f"An error occurred during the training process: {e}")

