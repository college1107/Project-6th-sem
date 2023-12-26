from User.models import *


def Insert(en_no, attended):
    a = attending_class.objects.create(en_no=en_no, attended=attended)
    return a
