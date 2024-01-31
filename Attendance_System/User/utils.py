from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from college_admin.models import *


def Insert(en_no):
    register.objects.filter(en_no=en_no).update(attended=True)


def Detect_Face(img_data):
    img = Image.open(BytesIO(img_data))
    print(img)
    img_array = np.array(img)

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(img_array, scaleFactor=1.05, minNeighbors=10)

    #  if not faces:
    #    return None

    for i, (x, y, w, h) in enumerate(faces):
      #   if 200 < w < img_array.shape[1] and 200 < h < img_array.shape[0]:
            face_roi = img_array[y : y + h + 20, x : x + w]
            pil_detected_face = Image.fromarray(face_roi)
            # pil_detected_face.save("detected_face_pil.jpg")
            return face_roi
        
