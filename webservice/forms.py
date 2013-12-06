from django import forms
import django.contrib.auth as django_auth

from webservice.models import Department, Course, \
        Task, TaskFile, CourseSession, StudentEnrollment, \
        SubmitRequest, StudentAnswerFile, StudentAnswerTestResult, StudentAnswer


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'shortName', 'description', 'department']

class CourseSessionForm(forms.ModelForm):
    class Meta:
        model = CourseSession
        fields = ['startDate', 'endDate', 'finished', 'course']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'public', 'courseSession']
        widgets = {
            'description': forms.Textarea(attrs={'rows':5})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        #FIXME: hack needed to make Textarea take the appropriate size
        self.fields['description'].widget.attrs['class'] = "input-block-level"

class TaskFileForm(forms.ModelForm):
    class Meta:
        model = TaskFile

class UserActivationForm(forms.Form):
    username = forms.CharField()
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(min_length=3, widget=forms.PasswordInput)
    newPasswordRepeat = forms.CharField(min_length=3, widget=forms.PasswordInput)
    def clean(self):
        print("Clean invoked")
        cleanedData = super(UserActivationForm, self).clean()
        usernameClean = cleanedData.get("username")
        oldPasswordClean = cleanedData.get("oldPassword")
        user = django_auth.authenticate(username=usernameClean, password=oldPasswordClean)
        if user is None:
            raise forms.ValidationError("No such user.")
        self.user = user
        newPasswordClean = cleanedData.get("newPassword")
        newPasswordRepeatClean = cleanedData.get("newPasswordRepeat")
        if newPasswordClean != newPasswordRepeatClean:
            self.fields['newPassword'].error_messages["invalid"] = ""
            self.fields['newPasswordRepeat'].error_messages["invalid"] = ""
            raise forms.ValidationError("New passwords must match.")
