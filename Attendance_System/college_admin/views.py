from django.shortcuts import render

# Create your views here.
def CA_home(request):
    return render(request,'CA_index.html')