from django.shortcuts import render, redirect
from django.contrib import messages
from college_admin.models import register
from User.models import attending_class
from User.utils import *
import cv2
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from skimage.metrics import structural_similarity as ssim
from skimage import io
from io import BytesIO
from PIL import Image
import requests
import numpy as np
import base64


class VideoCapture:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()


def video_feed():
    video_capture = VideoCapture()
    while True:
        frame = video_capture.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


def video(request):
    response = StreamingHttpResponse(
        video_feed(), content_type="multipart/x-mixed-replace; boundary=frame"
    )
    return response


def U_home(request):
    context = {"page": "Attendance", "color": "info"}
    if request.method == "POST":
        en_no = str(request.POST.get("en_no"))
        en_no = en_no.upper()
        context = {"page": "Attendance", "color": "info"}
        video_capture = VideoCapture()
        frame = video_capture.get_frame()
        # with open("img.jpg", "wb") as f:
        #     f.write(frame)
        if en_no == "":
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)
        # ****************************************************************************************************
        db_img, similarity_index = None, None

        if register.objects.filter(en_no=en_no).exists():
            if register.objects.filter(en_no=en_no, attended=False).exists():
                img_data = register.objects.get(en_no=en_no, attended=False).img.read()
                db_img = Detect_Face(img_data)
                print(db_img)
                db_img_array = np.array(db_img)

                if db_img is not None:
                    capture_img = Detect_Face(np.array(frame).tobytes())
                    cv2.imwrite('output_image.jpg', capture_img)
                    mse = np.sum((db_img_array - capture_img) ** 2) / float(
                        db_img_array.size
                    )
                    normalized_mse = mse / 255**2
                    print(normalized_mse)
                    print(f"Similarity Index: {mse}")

                similarity_threshold = 0.01

                if (
                    similarity_index is not None
                    and normalized_mse <= similarity_threshold
                ):
                    Insert(en_no)
                    return render(request, "U_success.html")
                else:
                    messages.success(request, "Sorry, Wrong Person")
                    context.update({"color": "danger"})
                    return render(request, "U_index.html", context)
            # ****************************************************************************************************
            else:
                messages.success(request, "Already attended")
                context.update({"color": "danger"})
                return render(request, "U_index.html", context)
        else:
            messages.success(request, "Not registered in DB")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)

    return render(request, "U_index.html", context)


def empty_db(request):
    try:
        register.objects.all().update(attended=False)
        messages.success(request, "All Registered student are set to False.")
    except Exception as e:
        messages.error(request, f"Error clearing database: {str(e)}")
    return redirect("U_home")
