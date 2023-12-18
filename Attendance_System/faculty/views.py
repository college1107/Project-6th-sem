from django.shortcuts import render

# Create your views here.
def F_home(request):
    return render(request,'F_index.html')