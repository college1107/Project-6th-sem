from django.shortcuts import render

# Create your views here.
def U_home(request):
    return render(request,'U_index.html')

def register(request):
    return render (request,'registration.html')