from django.shortcuts import render,redirect
from django.contrib import messages
from college_admin.models import register
from User.models import attending_class
from User.utils import Insert
from ipware import get_client_ip
import requests

# Create your views here.
def U_home(request):
    client_ip = request.META.get('REMOTE_ADDR')
    if client_ip:
        # Make a request to the IP geolocation API
        access_key = '17bbc22a35afbb5ad7ebce4fe74b56c2'
        api_url = f'http://api.ipstack.com/{client_ip}?access_key={access_key}'
        
        # Perform the API request
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            geolocation_data = response.json()
            print(f"Client's IP address: {client_ip}, Geolocation Data: {geolocation_data}")
        else:
           print(f"Failed to fetch geolocation data. Status Code: {response.status_code}")
    else:
        print("Unable to get the client's IP address")
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