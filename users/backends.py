from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                raise ValidationError("wrong password")
        except get_user_model().DoesNotExist:
            raise get_user_model().DoesNotExist

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
