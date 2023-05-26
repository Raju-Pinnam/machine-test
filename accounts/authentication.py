from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthBackend(object):
    """ Authententiaction Of user
        with email and userrname
    Args:
        object ([type]): user object
    """

    def authenticate(self, request, username=None, password=None):
        """
            Gets the user details here username is either username or email(appropriate field)
            if user matches with details and password it returns the user or None
        """
        try:
            user_obj = User.objects.get(username=username)
            return user_obj if user_obj.check_password(password) else None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        User ID is taking from authenticate returned user, and return the user
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
