from django.core.urlresolvers import reverse
from webservice.models import Course

def getShared(request):
    s = {
        'menu' : mainMenu(request),
        'courses' : getCourses(request)
    }
    return s

def mainMenu(request):
    menus = [
    ]
    adminMenu = {
        "name":"Admin",
        "view":"/admin",
        "submenu":[],
    }

    if request.user.is_superuser:
        menus.append(adminMenu)
    return menus

def getCourses(request):
    courses = []
    for v in Course.objects.all():
        courses.append(v)
    return courses
