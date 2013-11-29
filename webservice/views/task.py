from django.forms.models import modelformset_factory, formset_factory, HiddenInput
from django.forms import ModelChoiceField
from django.shortcuts import  render, redirect, HttpResponse
from django.utils import simplejson as json

from webservice.models import Task, TaskFile, CourseSession, CourseSessionTeacher
from webservice.forms import TaskForm, TaskFileForm
from webservice.views.shared import getShared

def userIsTeacher(user, courseSession):
    teachers = CourseSessionTeacher.objects.filter(courseSession=courseSession)
    teachers = [teacher.user for teacher in teachers]
    return user in teachers

def getFormErrors(form):
    return dict(form.error.items())

def createAjax(request, courseSessionId):
    data = {"success":False} 

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            data["success"] = True
            data["id"] = task.id
        else:
            data["errors"] = form.errors.items()

    return HttpResponse(json.dumps(data), mimetype='application/json')

def addTaskFiles(request, taskId):
    data = {"success":False} 

    if request.method == 'POST':
        form = TaskFile(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            data["success"] = True
            data["id"] = task.id
        else:
            data["errors"] = form.errors.items()

    return HttpResponse(json.dumps(data), mimetype='application/json')
    

def create(request, courseSessionId):
    #TODO: check if there is no such course session
    courseSession = CourseSession.objects.get(id=courseSessionId)
    course = courseSession.course
    
    if not userIsTeacher(request.user, courseSession):
        return redirect('webservice.views.course.read', id=course.id)

    print(request.FILES)
    TaskFileFormSet = formset_factory(TaskFileForm, max_num=10)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        taskFileFormset = TaskFileFormSet(request.POST, request.FILES)
        if form.is_valid() and taskFileFormset.is_valid():
            task = form.save()
            for taskFileForm in taskFileFormset.forms:
                taskFile = taskFileForm.save(commit=False)
                taskFile.task = task
                taskFile.save()
            return redirect('webservice.views.course.read', id=courseSession.course.id)
    else:
        form = TaskForm() # An unbound form
        taskFileFormset = TaskFileFormSet()

    form.fields['courseSession'].initial = courseSessionId
    form.fields['courseSession'].widget = HiddenInput()
    return render(request,
                  'task/create.html',
                  {'form':form, 'taskFileFormset':taskFileFormset, 
                   'courseSession':courseSession, 'course':course,
                   'shared':getShared(request)})

def fileDownload(request, id, fileName):
    task = Task.objects.get(id=id)
    course = task.courseSession.course

    filePath = "task_file/task_file/" + str(id) + "/" + fileName
    taskFile = TaskFile.objects.get(task=task, taskFile=filePath)

    if (not task.public or taskFile.isTestFile) and \
            not userIsTeacher(request.user, task.courseSession):
        return redirect('webservice.views.course.read', id=course.id)

    response = HttpResponse(taskFile.taskFile, content_type='text/plain')
    response['Content-Length'] = len(response.content)
    response['Content-Disposition'] = 'attachment; filename=' + fileName 
    return response

def read(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    task = Task.objects.get(id=id)
    taskFiles = TaskFile.objects.filter(task=task)
    for taskFile in taskFiles:
        print(taskFile.taskFile)
    course = task.courseSession.course
    return render(request,
                  'task/read.html',
                  {'task':task, 'taskFiles':taskFiles, 'course':course, 
                   'layout':layout, 'shared':getShared(request)})


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
                  {'task':task, 'form':form, 'layout':layout, 'shared':getShared(request)})

def delete(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    task = Task.objects.get(id=id)
    course = task.courseSession.course

    if not userIsTeacher(request.user, task.courseSession):
        return redirect('webservice.views.course.read', id=course.id)

    task.delete()

    return redirect('webservice.views.course.read', id=course.id)
