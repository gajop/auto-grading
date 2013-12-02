import django.contrib.auth as django_auth
from django.shortcuts import  render, redirect
from webservice.views.shared import getShared

def login(request):
    django_auth.logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = django_auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                django_auth.login(request, user)
                return redirect('webservice.views.course.index')
            else:
                return redirect('webservice.views.auth.activate')
    return redirect('webservice.views.course.index')

def logout(request):
    django_auth.logout(request)
    return redirect('webservice.views.course.index')

def activate(request):
    err = username = password1 = password2 = oldpassword = None
    django_auth.logout(request)
    if request.POST:
        username = request.POST['username']
        oldpassword = request.POST['oldpassword']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            err = "Passwords aren't matching"
        elif len(password1) < 3:
            err = "Password must be at least 3 characters long"            
        else:
            user = django_auth.authenticate(username=username, password=oldpassword)
            if user is not None:    
                if not user.is_active:
                    user.set_password(password1)
                    user.is_active = True
                    user.save()
                    django_auth.login(request, user)
                    return redirect('webservice.views.course.index')
                else: #user is already active, wrong!
                    return redirect('webservice.views.course.index')
    
    return render(request, 'registration/activate.html', 
            {'err':err, 'username':username, 'oldpassword':oldpassword, 'password1':password1, 'password2':password2, 'shared':getShared(request)})

