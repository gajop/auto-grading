from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy

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
    username = forms.CharField(label=_lazy("Username"))
    oldPassword = forms.CharField(label=_lazy("Old password"), widget=forms.PasswordInput)
    newPassword = forms.CharField(label=_lazy("New password"), min_length=3, widget=forms.PasswordInput)
    newPasswordRepeat = forms.CharField(label=_lazy("Repeat new password"), min_length=3, widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(UserActivationForm, self).clean()
        usernameClean = cleaned_data.get("username")
        oldPasswordClean = cleaned_data.get("oldPassword")
        user = django_auth.authenticate(username=usernameClean, password=oldPasswordClean)
        if user is None:
            raise forms.ValidationError(_("No such user."))
        self.user = user
        newPasswordClean = cleaned_data.get("newPassword")
        newPasswordRepeatClean = cleaned_data.get("newPasswordRepeat")
        if newPasswordClean != newPasswordRepeatClean:
            self._errors['newPassword'] = self.error_class([""])
            self._errors['newPasswordRepeat'] = self.error_class([""])
            raise forms.ValidationError(_("New passwords must match."))
        return cleaned_data
