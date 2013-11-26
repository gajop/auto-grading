import django.contrib.auth as django_auth
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect
from webservice.views.shared import getShared

def login(request):
    django_auth.logout(request)
    form = AuthenticationForm(data=request.POST)
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = django_auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_auth.login(request, user)
                    return redirect('webservice.views.course.index')
    return render(request, 'registration/login.html', 
            {'form':form, 'shared':getShared()})

def logout(request):
    django_auth.logout(request)
    return redirect('webservice.views.course.index')
