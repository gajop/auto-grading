from django.core.urlresolvers import reverse

def mainMenu():
    menus = []
    # TODO:
    # if user logged in... account settings
    # else sign in/register

    menus.append({
                  "name" : 'Courses',
                  "view" : reverse('webservice.views.course.index'),
                  "submenu" : []
      })
    tasksMenu = {
                  "name" : 'Tasks',
                  "view" : reverse('webservice.views.task.index'),
                  "submenu" : []
      }    
    if True: # TODO: change this with proper authorization check
        tasksMenu["submenu"].append({
                                   "name" : "Add",
                                   "view" : reverse("webservice.views.task.create"),
                                   "submenu" : [],                               
                                   })    

    menus.append(tasksMenu)
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
    pass