import cv2
import time
import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import Image, ImageTk
from database import getProfile
from main import main as run_main_function

def add_patient():
    # Initialize the face detector and recognizer
    facedetect = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/trainingdata.yml")

    # Capture start time
    start_time = time.time()
    capture_duration = 5  # Duration to capture faces in seconds

    # Initialize the camera for capturing images
    window_name = "Face Detection"
    should_run_main_function = False
    existing_patient_id = None

    # Open video capture
    cam = cv2.VideoCapture(0)

    while time.time() - start_time < capture_duration:
        ret, img = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image from camera.")
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    
            # Check if a profile exists for the predicted ID
            profile = getProfile(id)
            if profile is not None:
                existing_patient_id = profile[0]
                cv2.putText(img, "ID : "+str(profile[0]), (x, y+h+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127), 2)
                cv2.putText(img, "Name : "+str(profile[1]).title(), (x, y+h+55), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127), 2)
                cv2.putText(img, "Age : "+str(profile[2]), (x, y+h+80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127), 2)
                # cv2.putText(img, "Gender : "+str(profile[3]).title(), (x, y+h+110), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127), 2)

                should_run_main_function = True
            else:
                cv2.putText(img, "New Patient", (x, y+h+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                should_run_main_function = True

        # Convert the frame to PIL Image format and update the Tkinter label
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
        # Update the Tkinter window
        top.update()

        if cv2.waitKey(1) == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cam.release()
    cv2.destroyAllWindows()

    if should_run_main_function:
        top.destroy()
        run_main_function(existing_patient_id)

def open_toplevel(parent):
    global top, video_label
    # Create a Toplevel window
    top = Toplevel(parent)
    top.title("Video Stream")
    
    # Create a label to display the video feed
    video_label = tk.Label(top)
    video_label.pack()

    # Start the patient addition process
    add_patient()


# # Open the Toplevel window with video feed immediately
# open_toplevel()
