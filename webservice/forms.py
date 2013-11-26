from django.forms import ModelForm

from webservice.models import Department, Course, Student, \
        Task, TaskFile, CourseSession, StudentEnrollment, \
        SubmitRequest, StudentAnswerFile, StudentAnswerTestResult, StudentAnswer


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'shortName', 'description', 'department']

class CourseSessionForm(ModelForm):
    class Meta:
        model = CourseSession
        fields = ['startDate', 'endDate', 'finished', 'course']
        
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'public', 'courseSession']
