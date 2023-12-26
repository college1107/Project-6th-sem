from django.shortcuts import render
from django.contrib import messages
from college_admin.models import register

# Create your views here.
def U_home(request):
    context = {"page": "Attendance", "color": "info"}
    if request.method == "POST":
        data = request.POST
        en_no = data.get("en_no")
        # date = data.get("date")
        print(en_no)
        if en_no == "":
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)
        if register.objects.filter(en_no=en_no).exists():
            return render(request, "U_success.html", context)
        else:
            messages.success(request, f"Sorry {en_no} you are not registered in DB")
            context.update({"color": "danger"})
            return render(request,'U_index.html')

    return render(request,'U_index.html')

def success_page(request):
    return render(request, "U_success.html")