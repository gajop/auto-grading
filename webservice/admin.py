from django.contrib import admin
from webservice.models import Department, Course, Student, FileFormat, CourseFileFormat, \
        CourseSession, CourseSessionTeacher, StudentEnrollment, Task, TaskFile, \
        SubmitRequest, StudentAnswerFile, StudentAnswerTestResult, StudentAnswer

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(FileFormat)
admin.site.register(CourseFileFormat)

admin.site.register(CourseSession)
admin.site.register(CourseSessionTeacher)
admin.site.register(StudentEnrollment)
admin.site.register(Task)
admin.site.register(TaskFile)

admin.site.register(SubmitRequest)
admin.site.register(StudentAnswer)
admin.site.register(StudentAnswerFile)
admin.site.register(StudentAnswerTestResult)
