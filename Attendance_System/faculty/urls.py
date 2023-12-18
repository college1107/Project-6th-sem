
from django.urls import path
from faculty.views import *
urlpatterns = [
    path('',F_home,name='F_home'),
]
