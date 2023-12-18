
from django.urls import path
from college_admin.views import *
urlpatterns = [
    path('',CA_home,name='CA_home'),
]
