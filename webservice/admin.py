from django.contrib import admin
from webservice.models import Department, Course, Student, \
        Task, CourseSession, StudentEnrollment, \
        StudentAnswerFile, StudentAnswerTestResult, StudentAnswer

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Student)

admin.site.register(Task)
admin.site.register(CourseSession)
admin.site.register(StudentEnrollment)

admin.site.register(StudentAnswerFile)
admin.site.register(StudentAnswerTestResult)
admin.site.register(StudentAnswer)
