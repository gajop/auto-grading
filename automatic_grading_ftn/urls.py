from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group, Permission

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
class UserViewSet(viewsets.ModelViewSet):
    model = User            
class PermissionViewSet(viewsets.ModelViewSet):
    model = Permission           
class GroupViewSet(viewsets.ModelViewSet):
    model = Group            
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
router.register(r'rest/departments', DepartmentViewSet)
router.register(r'rest/courses', CourseViewSet)
router.register(r'rest/users', UserViewSet)
router.register(r'rest/permissions', PermissionViewSet)
router.register(r'rest/groups', GroupViewSet)

router.register(r'rest/courseSessions', CourseSessionViewSet)
router.register(r'rest/studentEnrollments', StudentEnrollmentViewSet)
router.register(r'rest/tasks', TaskViewSet)
router.register(r'rest/taskFiles', TaskFileViewSet)

router.register(r'rest/submitRequests', SubmitRequestViewSet)
router.register(r'rest/studentAnswers', StudentAnswerViewSet)
router.register(r'rest/studentAnswerTestResults', StudentAnswerTestResultViewSet)
router.register(r'rest/studentAnswerFiles', StudentAnswerFileViewSet)

urlpatterns = patterns('',
    url(r'^$', 'webservice.views.course.index'),
    url(r'^', include(router.urls)),

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
    url(r'^rest/create_user/', 'webservice.views.custom.create_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
