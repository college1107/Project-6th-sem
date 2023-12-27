from django.shortcuts import render
from college_admin.models import *
from User.models import *
import time
from datetime import datetime  # Import the datetime module

def F_home(request):
    data = register.objects.values('en_no', 'name', 'attended')
    
    current_time = time.localtime()
    current_datetime = datetime.fromtimestamp(time.mktime(current_time))

    context = {
        'data': data,
        'current_datetime': current_datetime,
    }
    return render(request, 'F_index.html', context)
