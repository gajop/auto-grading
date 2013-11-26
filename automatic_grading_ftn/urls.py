from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from webservice.models import Department, Course, Student, \
        Task, TaskFile, CourseSession, StudentEnrollment, \
        SubmitRequest, StudentAnswerFile, StudentAnswerTestResult, StudentAnswer
from rest_framework import viewsets, routers

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#static models
class DepartmentViewSet(viewsets.ModelViewSet):
    model = Department
class CourseViewSet(viewsets.ModelViewSet):
    model = Course
class StudentViewSet(viewsets.ModelViewSet):
    model = Student
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
router.register(r'students', StudentViewSet)

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

    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'webservice.views.auth.logout'),

    url(r'^courses/$',                       'webservice.views.course.index'),
    url(r'^courses/create/$',                'webservice.views.course.create'),
    url(r'^courses/(?P<id>\d+)/$',           'webservice.views.course.read'),
    url(r'^courses/update/(?P<id>\d+)/$',    'webservice.views.course.update'),
    url(r'^courses/delete/(?P<id>\d+)/$',    'webservice.views.course.delete'),

    url(r'^courseSessions/$',                       'webservice.views.course_session.index'),
    url(r'^courseSessions/create/$',                'webservice.views.course_session.create'),
    url(r'^courseSessions/(?P<id>\d+)/$',           'webservice.views.course_session.read'),
    url(r'^courseSessions/update/(?P<id>\d+)/$',    'webservice.views.course_session.update'),
    url(r'^courseSessions/delete/(?P<id>\d+)/$',    'webservice.views.course_session.delete'),

    url(r'^tasks/(?P<courseSessionId>\d+)/create/$',    'webservice.views.task.create'),
    url(r'^tasks/(?P<id>\d+)/$',                        'webservice.views.task.read'),
    url(r'^tasks/update/(?P<id>\d+)/$',                 'webservice.views.task.update'),
    url(r'^tasks/delete/(?P<id>\d+)/$',                 'webservice.views.task.delete'),

    url(r'^submit_answer/', 'webservice.views.custom.submit_answer'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
