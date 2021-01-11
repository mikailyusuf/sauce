from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, phone_number=None, first_name=None, last_name=None, password=None, ):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        # if phone_number is None:
        #     raise TypeError('Users should have a phone_number')
        #
        # if first_name is None:
        #     raise TypeError('Users should have a phone_number')
        #
        # if last_name is None:
        #     raise TypeError('Users should have a phone_number')

        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number,
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255,null=True,db_index=True)
    last_name = models.CharField(max_length=255,null=True, db_index=True)
    phone_number = models.CharField(max_length=30,null=True,db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
