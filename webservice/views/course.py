from django.forms.models import modelformset_factory
from django.db.models import Max
from django.shortcuts import  render, redirect
from webservice.models import Course, CourseSession, Task
from webservice.forms import CourseForm
from webservice.views.shared import getShared

def index(request):
    layout = request.GET.get('layout')
    courses = []
    for v in Course.objects.all():
#        try:
#            v.image = EventImage.objects.get(event=v).image
#        except EventImage.DoesNotExist:
#            pass #oh well
        courses.append(v)
    return render(request,
                  'course/index.html',
                  {'courses': courses, 'layout': layout, 'shared':getShared()} )

def create(request):
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
                  {'form':form, 'layout':layout, 'shared':getShared()})

def read(request, id):
    layout = request.GET.get('layout', 'horizontal')
    if not Course.objects.filter(id=id).exists():
        return redirect('webserviceApp.views.course.index')

    course = Course.objects.get(id=id)
    currentCourseSession = CourseSession.objects.filter(course=course, finished=False).order_by('startDate')[0]

    tasks = []
    for v in Task.objects.filter(courseSession=currentCourseSession):
        tasks.append(v)

    return render(request,
                  'course/read.html',
                  {'course':course, 'tasks':tasks, 'layout':layout, 'shared':getShared()})


def update(request, id):
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
                  {'Course' : course, 'layout': layout, 'form': form, 'shared':getShared()} )

def delete(request, id):
    layout = request.GET.get('layout')
    if not Course.objects.filter(id=id).exists():
        return redirect('webservice.views.course.index')

    course = Course.objects.get(id=id)
    course.delete()

    return redirect('webservice.views.course.index', { 'layout': layout })
