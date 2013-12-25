from django.shortcuts import  render, redirect
from django.utils.translation import ugettext as _

from django.views.decorators.csrf import csrf_exempt
from django.utils import translation

from django.contrib import messages
import django.contrib.auth as django_auth

from webservice.views.shared import getShared
from webservice.forms import LTILaunchForm
from webservice.models import LTIUser, LTICourse, User, Course, CourseSession, CourseSessionTeacher, StudentEnrollment

@csrf_exempt
def lti_launch(request):
    if request.method == 'POST':
        form = LTILaunchForm(request.POST)
        if form.is_valid():
            lti_message_type = form.cleaned_data['lti_message_type']
            lti_version = form.cleaned_data['lti_version']
            resource_link_id = form.cleaned_data['resource_link_id']

            #set locale
            try:
                locale = form.cleaned_data['launch_presentation_locale']
                #FIXME: isn't properly setting the user language
                translation.activate(locale) 
            except Excetion as e:
                print(e)
            
            #get course info
            try:
                context_id = form.cleaned_data["context_id"]                
                context_type = form.cleaned_data["context_type"]
                context_title = form.cleaned_data["context_title"]
                context_label = form.cleaned_data["context_label"]
                try:
                    ltiCourse = LTICourse.objects.get(context_id = context_id)
                    course = ltiCourse.course
                    courseSessions = CourseSession.objects.filter(course=course, finished=False).order_by('startDate')
                    courseSession = courseSessions[0]
                except:
                    course = Course(name = context_title, shortName = context_label)
                    course.save()
                    courseSession = CourseSession(course = course)
                    courseSession.save()
                    ltiCourse = LTICourse(context_id = context_id, course = course)
                    ltiCourse.save()
            except Exception as e:
                print(e)

            #get user info
            try:
                user_id = form.cleaned_data["user_id"]
                user_first_name = form.cleaned_data["lis_person_name_given"]
                user_last_name = form.cleaned_data["lis_person_name_family"]
                try:
                    ltiUser = LTIUser.objects.get(lti_user_id = user_id)
                    user = ltiUser.user
                except:
                    #FIXME: make sure the username isn't taken already
                    user = User.objects.create_user(username="lti_"+user_id, first_name=user_first_name, last_name=user_last_name)
                    user.save()
                    ltiUser = LTIUser(user = user, lti_user_id = user_id)
                    ltiUser.save()
                django_auth.logout(request)
                user = django_auth.authenticate(lti_user_id=user_id)
                django_auth.login(request, user)
                request.session['using_lti'] = True
            except Exception as e:
                print(e)
            
            #get user roles
            try:
                for role in form.cleaned_data["roles"].split(","):
                    if role.lower() == "instructor":
                        try:
                            teachers = CourseSessionTeacher.objects.filter(courseSession=courseSession)
                            teachers = [teacher.user for teacher in teachers]
                            if user not in teachers:
                                courseSessionTeacher = CourseSessionTeacher(courseSession=courseSession, user=user)
                                courseSessionTeacher.save()

                        except Exception as e:
                            print(e)
                    elif role.lower() == "learner":
                        try:
                            studentEnrollment = StudentEnrollment.objects.get(student=user, courseSession=courseSession)
                        except:
                            studentEnrollment = StudentEnrollment(student=user, courseSession=courseSession)
                            studentEnrollment.save()

            except Exception as e:
                print(e)

            if course:
                return redirect('webservice.views.course.read', course.id)
    return redirect('webservice.views.course.index')
