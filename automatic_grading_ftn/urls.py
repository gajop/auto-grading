from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, routers
from webservice.models import Department, Course,  \
        Task, TaskFile, CourseSession, StudentEnrollment, \
        SubmitRequest, StudentAnswerFile, StudentAnswerTestResult, StudentAnswer

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#static models
class DepartmentViewSet(viewsets.ModelViewSet):
    model = Department
class CourseViewSet(viewsets.ModelViewSet):
    model = Course
#semester dynamic models
class CourseSessionViewSet(viewsets.ModelViewSet):
    model = CourseSession
class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    model = StudentEnrollment
class TaskViewSet(viewsets.ModelViewSet):
    model = Task
class TaskFileViewSet(viewsets.ModelViewSet):
    model = TaskFile
#course dynamic models
class SubmitRequestViewSet(viewsets.ModelViewSet):
    model = SubmitRequest
class StudentAnswerViewSet(viewsets.ModelViewSet):
    model = StudentAnswer
class StudentAnswerTestResultViewSet(viewsets.ModelViewSet):
    model = StudentAnswerTestResult
class StudentAnswerFileViewSet(viewsets.ModelViewSet):
    model = StudentAnswerFile

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)

router.register(r'courseSessions', CourseSessionViewSet)
router.register(r'studentEnrollments', StudentEnrollmentViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'taskFiles', TaskFileViewSet)

router.register(r'submitRequests', SubmitRequestViewSet)
router.register(r'studentAnswers', StudentAnswerViewSet)
router.register(r'studentAnswerTestResults', StudentAnswerTestResultViewSet)
router.register(r'studentAnswerFiles', StudentAnswerFileViewSet)

urlpatterns = patterns('',
    url(r'^$', 'webservice.views.course.index'),

    (r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^login$',  'webservice.views.auth.login'),
    url(r'^activate$',  'webservice.views.auth.activate'),
    url(r'^logout$', 'webservice.views.auth.logout'),

    url(r'^courses/$',                       'webservice.views.course.index'),
    url(r'^courses/create/$',                'webservice.views.course.create'),
    url(r'^courses/(?P<id>\d+)/$',           'webservice.views.course.read'),
    url(r'^courses/update/(?P<id>\d+)/$',    'webservice.views.course.update'),
    url(r'^courses/delete/(?P<id>\d+)/$',    'webservice.views.course.delete'),

    url(r'^course/(?P<courseSessionId>\d+)/addTask/$',  'webservice.views.task.create'),
    url(r'^task/(?P<id>\d+)/$',                         'webservice.views.task.read'),
    url(r'^task/(?P<id>\d+)/files/(?P<fileName>[^/]+)', 'webservice.views.task.fileDownload'),
    url(r'^task/update/(?P<id>\d+)/$',                  'webservice.views.task.update'),
    url(r'^task/delete/(?P<id>\d+)/$',                  'webservice.views.task.delete'),
    url(r'^task/(?P<id>\d+)/submitAnswer/$',            'webservice.views.task.submitAnswer'),

    url(r'^submit_answer/', 'webservice.views.custom.submit_answer'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
