from django.core.urlresolvers import reverse
from webservice.models import Course, StudentEnrollment, Student

def getShared():
    s = {
        'menu' : mainMenu(),
        'courses' : getCourses()
    }
    return s

def mainMenu():
    menus = [
    ]
    # TODO:
    # if user logged in... account settings
    # else sign in/register
    """
    eventsMenu = {
          "name" : 'Events',
          "view" : reverse('webservice.views.event.index'),
          "submenu" : []
    }
    eventsMenu["submenu"].append({
                       "name" : "Add",
                       "view" : reverse("webservice.views.event.create"),
                       "submenu" : [],
    })
    menus.append(eventsMenu)
    """
    return menus

def getCourses():
    courses = []
    for v in Course.objects.all():
        courses.append(v)
    return courses
