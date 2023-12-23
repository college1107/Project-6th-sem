from college_admin.models import *
import os

def Insert(en_no, name, image):
    a = register.objects.create(en_no=en_no, name=name, img=image)
    return a

import os

def Emptying(path):
    cwd = os.getcwd()
    abs_path = os.path.abspath(path)
    abs_path = abs_path.replace("\\", "/")
    print(os.listdir(abs_path))
    for i in os.listdir(abs_path):
        file_to_remove = os.path.join(abs_path, i)
        os.remove(file_to_remove)





# # Get the current working directory

# # Define the relative path to the file you want to remove

# # Construct the absolute path to the file

# # Remove the file
# os.remove(abs_path)