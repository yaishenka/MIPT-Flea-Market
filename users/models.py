from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager
from django.core.exceptions import ValidationError


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if email is not None:
            pass
            # TODO sen verification email

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_verified'] = True
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['full_name', 'email']
    USERNAME_FIELD = 'username'

    objects = UserAccountManager()

    username = models.CharField('username', unique=True, blank=False,
                                null=False, max_length=200)
    email = models.EmailField('email', unique=True, blank=True, null=False)
    full_name = models.CharField('full name', blank=False, null=True,
                                 max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField('superuser status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID',
                                         default=uuid.uuid4)
    mail_send = models.BooleanField(default=False)
    restore_password_uuid = models.UUIDField(default=None, blank=True,
                                             null=True)


from django.contrib.auth.backends import ModelBackend
class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = CustomUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                raise ValidationError("wrong password")
        except CustomUser.DoesNotExist:
            raise CustomUser.DoesNotExist

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
