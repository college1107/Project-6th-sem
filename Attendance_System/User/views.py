from django.shortcuts import render,redirect
from django.contrib import messages
from college_admin.models import register
from User.models import attending_class
from User.utils import Insert


# Create your views here.
def U_home(request):
    context = {"page": "Attendance", "color": "info"}
    if request.method == "POST":
        data = request.POST
        en_no = data.get("en_no")
        print(en_no)
        if en_no == "":
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)
        if register.objects.filter(en_no=en_no).exists():
            if attending_class.objects.filter(en_no=en_no).exists():
                messages.success(request, f"{en_no} already attended")
                return render(request, "U_index.html")
            else:
                Insert(en_no=en_no, attended=True)
            return render(request, "U_success.html", context)
        else:
            messages.success(request, f"Sorry {en_no} you are not registered in DB")
            context.update({"color": "danger"})
            return render(request, "U_index.html")

    return render(request, "U_index.html")

def empty_db(request):
    try:
        attending_class.objects.all().delete()
        messages.success(request, "DB cleared successfully.")
    except Exception as e:
        messages.error(request, f"Error clearing database: {str(e)}")
    return redirect("U_home")