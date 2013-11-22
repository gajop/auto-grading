from django.forms.models import modelformset_factory
from django.shortcuts import  render, redirect
from webservice.models import CourseSession
from webservice.forms import CourseSessionForm
from webservice.views.shared import getShared

def index(request):
    layout = request.GET.get('layout')
    course_sessions = []
    for v in CourseSession.objects.all():
#        try:
#            v.image = EventImage.objects.get(event=v).image
#        except EventImage.DoesNotExist:
#            pass #oh well
        course_sessions.append(v)
    return render(request,
                  'course_session/index.html',
                  {'course_sessions': course_sessions, 'shared':getShared()} )

def create(request):
    layout = request.GET.get('layout')
    if request.method == 'POST':
        form = CourseSessionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.course_session.index')
    else:
        form = CourseSessionForm() # An unbound form

    return render(request,
                  'course_session/create.html',
                  {'form': form, 'shared':getShared()} )

def read(request, id):
    layout = request.GET.get('layout')
    if not CourseSession.objects.filter(id=id).exists():
        return redirect('webservice.views.course_session.index')

    course_session = CourseSession.objects.get(id=id)
    return render(request,
                  'course_session/read.html',
                  {'course_session': course_session, 'shared':getShared()})


def update(request, id):
    layout = request.GET.get('layout')
    if not CourseSession.objects.filter(id=id).exists():
        return redirect('webservice.views.course_session.index')

    course_session = CourseSession.objects.get(id=id)
    if request.method == 'POST':
        form = CourseSessionForm(request.POST, request.FILES, instance=course_session)
        if form.is_valid():
            form.save()
            return redirect('webservice.views.course_session.index')
    else:
        form = CourseSessionForm(instance=course_session) # An unbound form

    return render(request,
                  'course_session/update.html',
                  {'CourseSession' : course_session, 'form': form, 'shared':getShared()} )

def delete(request, id):
    layout = request.GET.get('layout')
    if not CourseSession.objects.filter(id=id).exists():
        return redirect('webservice.views.course_session.index')

    course_session = CourseSession.objects.get(id=id)
    course_session.delete()

    return redirect('webservice.views.course_session.index')
