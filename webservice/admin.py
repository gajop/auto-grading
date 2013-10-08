from django.contrib import admin
from webservice.models import Department, Course, Student, \
        Task, CourseSession, StudentEnrollment, \
        SubmitRequestFiles, SubmitRequestTestResult, SubmitRequest

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Student)

admin.site.register(Task)
admin.site.register(CourseSession)
admin.site.register(StudentEnrollment)

admin.site.register(SubmitRequestFiles)
admin.site.register(SubmitRequestTestResult)
admin.site.register(SubmitRequest)
