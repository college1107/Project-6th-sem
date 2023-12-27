from college_admin.models import *


def Insert(en_no):
   register.objects.filter(en_no=en_no).update(attended=True)
