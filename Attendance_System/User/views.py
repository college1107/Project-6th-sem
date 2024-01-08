from django.shortcuts import render, redirect
from django.contrib import messages
from college_admin.models import register
from User.models import attending_class
from User.utils import Insert
import base64

# Create your views here.
def U_home(request):
    img=''
    context = {"page": "Attendance", "color": "info"}
    if request.method == "POST":
        image_data = request.POST.get("image_data")
        if image_data is None:
            pass
        else:
            img=image_data
        en_no = str(request.POST.get("en_no"))
        en_no=en_no.upper()
        if en_no == "" and image_data is None:
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)
        padding = "=" * ((4 - len(img) % 4) % 4)

# Add padding to the base64 string
        img_padded = img + padding
        image_data = base64.b64decode(img_padded)
        with open('img.jpg', 'wb') as f:
            f.write(image_data)
        if register.objects.filter(en_no=en_no).exists():
            if register.objects.filter(en_no=en_no, attended=False).exists():
                Insert(en_no)
                return render(request, "U_success.html")
            else:
                messages.success(request, "already attended")
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
