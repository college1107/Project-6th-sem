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
        en_no = en_no.upper()
        # print(en_no)
        if en_no == "":
            messages.success(request, "Missing Field's")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)
        if register.objects.filter(en_no=en_no).exists():
            if register.objects.filter(en_no=en_no,attended=False).exists():
                Insert(en_no)
                return render(request,"U_success.html")
            else:
                messages.success(request, "already attended")
                context.update({"color": "danger"})
                return render(request, "U_index.html", context)
        else:
            messages.success(request, "Not registered in DB")
            context.update({"color": "danger"})
            return render(request, "U_index.html", context)

    return render(request, "U_index.html",context)

def empty_db(request):
    try:
        register.objects.all().update(attended=False)
        messages.success(request, "All Registered student are set to False.")
    except Exception as e:
        messages.error(request, f"Error clearing database: {str(e)}")
    return redirect("U_home")