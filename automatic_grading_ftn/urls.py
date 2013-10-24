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
    # Examples:
    # url(r'^$', 'automatic_grading_ftn.views.home', name='home'),
    # url(r'^automatic_grading_ftn/', include('automatic_grading_ftn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^submit_answer/', 'webservice.views.submit_answer'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
