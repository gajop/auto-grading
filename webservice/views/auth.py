from django.shortcuts import  render, redirect
from django.utils.translation import ugettext as _

import django.contrib.auth as django_auth
from django.contrib import messages

from webservice.forms import UserActivationForm

from webservice.views.shared import getShared

def login(request):
    django_auth.logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = django_auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_auth.login(request, user)
                return redirect('webservice.views.course.index')
            else:
                return redirect('webservice.views.auth.activate')
        messages.error(request, _('Incorrect username or password.'))
    return redirect('webservice.views.course.index')

def logout(request):
    django_auth.logout(request)
    return redirect('webservice.views.course.index')

def activate(request):
    django_auth.logout(request)

    if request.method == 'POST':
        form = UserActivationForm(request.POST)
        if form.is_valid():
            user = form.user
            if not user.is_active:
                user.set_password(form.cleaned_data["newPassword"])
                user.is_active = True
                user.save()
                django_auth.login(request, user)
                messages.success(request, _("Account successfully activated."))
                return redirect('webservice.views.course.index')
            else: #user is already active, wrong!
                return redirect('webservice.views.course.index')
    else:
        messages.warning(request, _('Welcome! As this is your first login, you need to create a new password.'))
        form = UserActivationForm()

    return render(request, 'registration/activate.html',
            {'form':form, 'shared':getShared(request)})

