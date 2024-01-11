from django.shortcuts import render, redirect
from django.contrib import messages
from college_admin.models import register
from User.models import attending_class
from User.utils import Insert
import base64
import cv2
from django.http import StreamingHttpResponse
from django.http import HttpResponse


# Create your views here.
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


def index(request):
    return render(request, "index.html")


def video(request):
    response = StreamingHttpResponse(
        video_feed(), content_type="multipart/x-mixed-replace; boundary=frame"
    )
    return response


def capture(request):
    try:
        video_capture = VideoCapture()
        frame = video_capture.get_frame()

        with open("img.jpg", "wb") as f:
            f.write(frame)

        return redirect("/")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return HttpResponse("An error occurred.")


def U_home(request):
    context = {"page": "Attendance", "color": "info"}
    if request.method == "POST":
        en_no = str(request.POST.get("en_no"))
        en_no = en_no.upper()
        if en_no is None:
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)
        if register.objects.filter(en_no=en_no).exists():
            if register.objects.filter(en_no=en_no, attended=False).exists():
                Insert(en_no)
                return render(request, "U_success.html")
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
