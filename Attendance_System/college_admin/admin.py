from django.contrib import admin
from college_admin.models import *
# Register your models here.


class regAdmin(admin.ModelAdmin):
    list_display =  ('en_no','name','img')

admin.site.register(register,regAdmin)