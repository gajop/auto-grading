from django.forms.models import modelformset_factory, HiddenInput
from django.forms import ModelChoiceField
from django.shortcuts import  render, redirect
from webservice.models import Task, TaskFile, CourseSession, CourseSessionTeacher
from webservice.forms import TaskForm
from webservice.views.shared import getShared

def userIsTeacher(user, courseSession):
    teachers = CourseSessionTeacher.objects.filter(courseSession=courseSession)
    teachers = [teacher.user for teacher in teachers]
    return user in teachers


def create(request, courseSessionId):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'

    #TODO: check if there is no such course session
    courseSession = CourseSession.objects.get(id=courseSessionId)
    course = courseSession.course
    
    if not userIsTeacher(request.user, courseSession):
        return redirect('webservice.views.course.read', id=course.id)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.course.read', id=courseSession.course.id)
    else:
        form = TaskForm() # An unbound form

    form.fields['courseSession'].initial = courseSessionId
    form.fields['courseSession'].widget = HiddenInput()
    return render(request,
                  'task/create.html',
                  {'form':form, 'courseSession':courseSession, 'course':course,
                   'layout':layout, 'shared':getShared()})

def read(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    task = Task.objects.get(id=id)
    course = task.courseSession.course
    return render(request,
                  'task/read.html',
                  {'task':task, 'course':course, 'layout':layout, 'shared':getShared()})


def update(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    task = Task.objects.get(id=id)

    if not userIsTeacher(request.user, task.courseSession):
        return redirect('webservice.views.course.read', id=task.courseSession.course.id)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.course.index')
    else:
        form = TaskForm(instance=task) # An unbound form

    return render(request,
                  'task/update.html',
                  {'task':task, 'form':form, 'layout':layout, 'shared':getShared()})

def delete(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    task = Task.objects.get(id=id)

    if not userIsTeacher(request.user, task.courseSession):
        return redirect('webservice.views.course.read', id=course.id)

    course = task.courseSession.course
    task.delete()

    return redirect('webservice.views.course.read', id=course.id)
