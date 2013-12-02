from django.core.urlresolvers import reverse
from webservice.models import Course, CourseSessionTeacher, StudentEnrollment

def userIsTeacher(user, courseSession):
    teachers = CourseSessionTeacher.objects.filter(courseSession=courseSession)
    teachers = [teacher.user for teacher in teachers]
    return user in teachers

def studentIsEnrolled(student, courseSession):
    enrolled = False
    if student.is_authenticated():
        try:
            studentEnrollment = StudentEnrollment.objects.get(student=student, courseSession=courseSession)
            enrolled = True
        except StudentEnrollment.DoesNotExist:
            pass
    return enrolled


def getShared(request):
    courses = getCourses(request)
    enrolledCourses = [course for course in courses if course.enrolled]
    s = {
        'menu' : mainMenu(request),
        'enrolledCourses' : enrolledCourses,
        'courses' : courses
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
    courses = Course.objects.all()
    for course in courses:
        course.enrolled = False
    if request.user.is_authenticated():
        studentEnrollments = StudentEnrollment.objects.filter(student=request.user)
        for course in courses:
            if studentEnrollments.filter(courseSession__course__exact = course).count() > 0:
                course.enrolled = True
    return courses
