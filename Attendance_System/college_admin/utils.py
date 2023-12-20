from college_admin.models import *
def EmptyDB():
    a = input("Are you sure Y/N")
    if a=='y':
        register.objects.all().delete()

def Insert(en_no, name, image):
    a = register.objects.create(en_no=en_no, name=name, img=image)
    return a