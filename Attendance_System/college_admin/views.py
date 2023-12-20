from django.shortcuts import render
from college_admin.utils import *
from django.contrib import messages


def inserting(enno, name, image):
    a = Insert(enno, name, image)
    if a != None:
        return True


# Create your views here.
def CA_home(request):
    context = {
        "page": "Admin",
    }
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        en_no = data.get("en_no")
        img = request.FILES.get("image")
        if inserting(en_no, name, img) :
            messages.success(request, "Data Submitted")
            context.update({"color": "success"})
    return render(request, "CA_index.html",context)