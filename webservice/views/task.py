from django.forms.models import modelformset_factory
from django.shortcuts import  render, redirect
from webservice.models import Task, TaskFile
from webservice.forms import TaskForm
from webservice.views.shared import getShared

def index(request):
    layout = request.GET.get('layout')
    tasks = []
    for v in Task.objects.all():
        tasks.append(v)
    return render(request,
                  'task/index.html',
                  {'tasks':tasks, 'layout':layout, 'shared':getShared()})

def create(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.task.index')
    else:
        form = TaskForm() # An unbound form

    return render(request,
                  'task/create.html',
                  {'form':form, 'layout':layout, 'shared':getShared()})

def read(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.task.index')

    task = Task.objects.get(id=id)
    return render(request,
                  'task/read.html',
                  {'task':task,'layout':layout, 'shared':getShared()})


def update(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.task.index')

    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.task.index')
    else:
        form = TaskForm(instance=task) # An unbound form

    return render(request,
                  'task/update.html',
                  {'task':task, 'form':form, 'layout':layout, 'shared':getShared()})

def delete(request, id):
    layout = request.GET.get('layout')
    if not Task.objects.filter(id=id).exists():
        return redirect('webservice.views.task.index')

    task = Task.objects.get(id=id)
    task.delete()

    return redirect('webservice.views.task.index',
            {'layout':layout})
