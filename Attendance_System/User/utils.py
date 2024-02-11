from PIL import Image
from io import BytesIO
import numpy as np
from college_admin.models import *
from deepface import DeepFace


def Insert(en_no):
    register.objects.filter(en_no=en_no).update(attended=True)


img_data = None


def Detect_Face(en_no):
    register_entry = register.objects.get(en_no=en_no)

    img_data = register_entry.img.read()
    cap_img_data = register_entry.cap_img.read()
    image_frame = Image.open(BytesIO(cap_img_data))
    image_db = Image.open(BytesIO(img_data))
    image_frame_np = np.array(image_frame)
    image_db_np = np.array(image_db)
    result = DeepFace.verify(image_frame_np, image_db_np, enforce_detection=False)

    return result["verified"]
