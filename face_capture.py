# face_capture.py
import cv2

def capture_faces(Id):
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)

    sample_num = 0
    while True:
        ret, img = cam.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            sample_num += 1
            cv2.imwrite(f"dataset/User.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(400)
        
        cv2.imshow("Capturing Face", img)
        cv2.waitKey(1)
        
        if sample_num > 19:
            break
    
    # cam.release()
    # cv2.destroyAllWindows()

