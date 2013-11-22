import django.contrib.auth as django_auth
from webservice.views.shared import getShared

def login(request):
    layout = request.GET.get('layout', 'horizontal')
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_auth.login(request, user) # Redirect to a success page.
        else: # Return a 'disabled account' error message
            return render(request,
                          'registration/login.html',
                          {'tasks':tasks, 'layout':layout, 'shared':getShared()})
    else: # Return an 'invalid login' error message.
        pass

def logout(request):
    return render(request,
            'registration/login.html',
            {'tasks':tasks, 'layout':layout, 'shared':getShared()})
    django_auth.logout(request)
