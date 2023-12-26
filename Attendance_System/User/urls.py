
from django.urls import path
from User.views import *
urlpatterns = [
    path('',U_home,name='U_home'),
    path('empty_database/', empty_database, name='empty_database'),
]