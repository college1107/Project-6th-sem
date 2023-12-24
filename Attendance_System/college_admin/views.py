from django.shortcuts import render, redirect
from college_admin.utils import *
from django.contrib import messages
from college_admin.models import *
def inserting(enno, name, image):
    temp = Insert(enno, name, image)
    if temp != None:
        return True

def empty_database(request):
    try:
        register.objects.all().delete()
        Emptying()
        messages.success(request, "Database cleared successfully.")
    except Exception as e:
        messages.error(request, f"Error clearing database: {str(e)}")
    return redirect("CA_home")


def CA_home(request):
    context = {"page": "Admin", "color": "info"}  

    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        en_no = data.get("en_no")
        img = request.FILES.get("image")
        img_str = str(img)
        if name == "" or en_no == "" or img_str == 'None':
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "CA_index.html", context)
        elif img_str.split('.')[1]!='.jpeg' or img_str.split('.')[1]!='.png' or img_str.split('.')[1]!='.jpg':
            messages.success(request, "Image is not valid")
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
