from django.shortcuts import render, redirect
from college_admin.utils import *
from django.contrib import messages
from college_admin.models import *


def inserting(enno, name, image):
    a = Insert(enno, name, image)
    if a != None:
        return True


def empty_database(request):
    context = {"color": "success"}
    render(request, "CA_index.html", context)
    try:
        register.objects.all().delete()  
        messages.success(request, "Database cleared successfully.")
    except Exception as e:
        messages.error(request, f"Error clearing database: {str(e)}")
    # render(request, "CA_index.html",context)
    return redirect("CA_home")


def CA_home(request):
    context = {
        "page": "Admin",
    }

    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        en_no = data.get("en_no")
        img = request.FILES.get("image")

        if name=='' or en_no=='':
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "CA_index.html", context)
        if register.objects.filter(en_no=en_no).exists():
            messages.success(request, "Enrollment number is Primary Key in DB")
            context.update({"color": "danger"})
            return render(request, "CA_index.html", context)
        if inserting(en_no, name, img):
            messages.success(request, "Data Submitted")
            context.update({"color": "success"})

    return render(request, "CA_index.html", context)

