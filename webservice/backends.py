from webservice.models import LTIUser, User

class LTIBackend(object):
    def authenticate(self, lti_user_id=None):
        try:
            ltiUser = LTIUser.objects.get(lti_user_id = lti_user_id)
            user = ltiUser.user
            return user
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
