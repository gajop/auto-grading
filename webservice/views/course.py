from django.forms.models import modelformset_factory
from django.db.models import Max
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User
from webservice.models import Course, CourseSession, CourseSessionTeacher, Task, StudentAnswer
from webservice.forms import CourseForm
from webservice.views.shared import getShared, userIsTeacher

def index(request):
    layout = request.GET.get('layout')
    courses = []
    for v in Course.objects.all():
        courses.append(v)
    return render(request,
                  'course/index.html',
                  {'courses': courses, 'layout': layout, 'shared':getShared(request)} )

def create(request):
    if not request.user.is_superuser:
        return redirect('webservice.views.course.index')
    layout = request.GET.get('layout', 'horizontal')
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.course.index')
    else:
        form = CourseForm() # An unbound form

    return render(request,
                  'course/create.html',
                  {'form':form, 'layout':layout, 'shared':getShared(request)})

def read(request, id):
    layout = request.GET.get('layout', 'vertical')
    if not Course.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    course = Course.objects.get(id=id)
    courseSessions = CourseSession.objects.filter(course=course, finished=False).order_by('startDate')
    currentCourseSession = courseSessions[0]

    isTeacher = userIsTeacher(request.user, currentCourseSession)
    tasks = Task.objects.filter(courseSession=currentCourseSession)
    if not isTeacher:
        tasks = tasks.filter(public = True)

    #TODO: this could be too slow, revise maybe?
    if request.user.is_authenticated():
        studentAnswers = StudentAnswer.objects.filter(student = request.user)
        for task in tasks:
            task.success = False
            task.attempt = False
            correctAnswers = studentAnswers.filter(task=task, success=True)
            if correctAnswers.count() > 0:
                task.success = True
                task.attempt = True
            else:
                falseAnswers = studentAnswers.filter(task=task, success=False)
                if falseAnswers.count() > 0:
                    task.attempt = True

    return render(request,
                  'course/read.html',
                  {'course':course, 'tasks':tasks, 'courseSessions':courseSessions, 
                   'currentCourseSession':currentCourseSession, 'isTeacher':isTeacher, 
                   'layout':layout, 'shared':getShared(request)})


def update(request, id):
    if not request.user.is_superuser:
        return redirect('webservice.views.course.index')
    layout = request.GET.get('layout')
    if not Course.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    course = Course.objects.get(id=id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.course.index')
    else:
        form = CourseForm(instance=course) # An unbound form

    return render(request,
                  'course/update.html',
                  {'Course' : course, 'layout': layout, 'form': form, 'shared':getShared(request)} )

def delete(request, id):
    if not request.user.is_superuser:
        return redirect('webservice.views.course.index')
    layout = request.GET.get('layout')
    if not Course.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    course = Course.objects.get(id=id)
    course.delete()

    return redirect('webservice.views.course.index', { 'layout': layout })
