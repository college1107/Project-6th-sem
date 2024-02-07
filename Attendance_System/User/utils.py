from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from college_admin.models import *
from deepface import DeepFace
from django.core.files.base import ContentFile

def Insert(en_no):
    register.objects.filter(en_no=en_no).update(attended=True)


def Detect_Face(en_no,img_data):
    register_entry = register.objects.get(en_no=en_no)
    img = register_entry.img.read()
    if isinstance(img_data, str):
        img_data = img_data.encode('utf-8')
    image_frame = Image.open(BytesIO(img_data))
    image_db = Image.open(BytesIO(img))
    image_frame_np = np.array(image_frame)
    image_db_np = np.array(image_db)
    result = DeepFace.verify(image_frame_np, image_db_np, model_name="VGG-Face", enforce_detection=False)
    return result['verified']