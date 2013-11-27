from django.forms import ModelForm, Textarea

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
        widgets = {
            'description': Textarea(attrs={'rows':5})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = "input-block-level"

class TaskFileForm(ModelForm):
    class Meta:
        model = TaskFile
        exclude = ('task',)
