import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not password:
            password = None

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

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

    @property
    def get_full_name(self):
        if self.full_name is not None:
            return self.full_name

        return self.username

    @property
    def is_social_user(self):
        from social_django.models import UserSocialAuth
        try:
            social_user = UserSocialAuth.objects.get(user=self)
        except UserSocialAuth.DoesNotExist:
            return False

        return True
