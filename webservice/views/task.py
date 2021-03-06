import json

from django.forms.models import modelformset_factory, formset_factory, HiddenInput
from django.forms import ModelChoiceField
from django.shortcuts import  render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from webservice.models import Task, TaskFile, CourseSession, CourseSessionTeacher, CourseFileFormat, FileFormat, StudentEnrollment
from webservice.forms import TaskForm, TaskFileForm
from webservice.views.shared import getShared, userIsTeacher, studentIsEnrolled
from webservice.submit import processAnswer

def getFormErrors(form):
    return dict(form.error.items())

@login_required
def submitAnswer(request, id):
    task = Task.objects.get(id=id)
    enrolled = studentIsEnrolled(request.user, task.courseSession)
    if enrolled and request.method == 'POST':
        #list of tuples (filename, file)
        files = []
        for i, uploadedFile in enumerate(request.FILES.getlist('files[]')):
            filename = uploadedFile.name            
            files.append((filename, uploadedFile))
        result = processAnswer(task, request.user, files)
        if request.is_ajax():
            data = {"success":True, "result":result}
            return HttpResponse(json.dumps(data), content_type="application/json")

    return redirect('webservice.views.task.read', id=id)

def create(request, courseSessionId):
    #TODO: check if there is no such course session
    courseSession = CourseSession.objects.get(id=courseSessionId)
    course = courseSession.course
    
    if not userIsTeacher(request.user, courseSession):
        return redirect('webservice.views.course.read', id=course.id)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            for i, uploadedFile in enumerate(request.FILES.getlist('files[]')):
                taskFile = TaskFile(task=task)
                
                fileFormatName = 'form-' + str(i) + 'fileFormat'
                if fileFormatName in request.POST:
                    fileFormatID = int(request.POST[fileFormatName])
                    if fileFormatID != -1:
                        fileFormat = FileFormat.objects.get(pk=fileFormatID)
                        taskFile.fileFormat = fileFormat
                
                fileTypeName = 'form-' + str(i) + 'fileType'
                fileTypeID = int(request.POST[fileTypeName])
                if fileTypeID != -1:
                    taskFile.fileType = fileTypeID

                publicFileName = 'form-' + str(i) + 'publicFile'
                if publicFileName in request.POST and request.POST[publicFileName] == 'on':
                    publicFile = True
                else:
                    publicFile = False
                taskFile.public = publicFile

                filename = uploadedFile.name
                taskFile.taskFile.save(filename, uploadedFile)
                taskFile.save()
            if request.is_ajax():
                data = {"success":True} 
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                return redirect('webservice.views.course.read', id=courseSession.course.id)
        elif request.is_ajax():
            data = {}
            data["errors"] = form.errors.items()
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        form = TaskForm() # An unbound form
    
    form.fields['courseSession'].initial = courseSessionId
    form.fields['courseSession'].widget = HiddenInput()
    return render(request,
                  'task/create.html',
                  {'form':form, 'courseSession':courseSession,
                   'course':course, 'fileTypes':TaskFile.TYPE_CHOICES,
                   'shared':getShared(request)})

def fileDownload(request, id, fileName):
    task = Task.objects.get(id=id)
    course = task.courseSession.course

    filePath = "task_file/task_file/" + str(id) + "/" + fileName
    taskFile = TaskFile.objects.get(task=task, taskFile=filePath)

    if (not task.public or taskFile.fileType == TaskFile.T_TEST) and \
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
    course = task.courseSession.course
    isTeacher = userIsTeacher(request.user, task.courseSession)
    if not task.public and not isTeacher:
        return redirect('webservice.views.course.read', id=course.id)
    taskFiles = TaskFile.objects.filter(task=task)
    if not isTeacher:
        taskFiles = taskFiles.filter(public = True)

    enrolled = studentIsEnrolled(request.user, task.courseSession)

    return render(request,
                  'task/read.html',
                  {'task':task, 'taskFiles':taskFiles, 'course':course, 'isTeacher':isTeacher, 'enrolled':enrolled,
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
