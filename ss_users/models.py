from enum import Enum, unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.core.validators import MinLengthValidator
from ss_utils.validators import (NameValidator, PhoneValidator)
from ss_users.managers import UserManager

@unique
class UserRoles(Enum):
    USER = 'user'

    @staticmethod
    def from_str(role):
        for rol in UserRoles:
            if rol.value == role:
                return rol
        return None

    @staticmethod
    def group_from_str(role):
        rol = UserRoles.from_str(role)
        if rol is None:
            return None
        else:
            return Group.objects.get(name=rol.value)

class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=255, validators=[
        NameValidator("first_name"), MinLengthValidator(2)])
    middle_name = models.CharField(max_length=255, blank=True, validators=[
        NameValidator("middle_name")])
    last_name = models.CharField(max_length=255, validators=[
        NameValidator("last_name"), MinLengthValidator(2)])
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    mobile = models.CharField(max_length=15, unique=True, validators=[
        PhoneValidator("mobile", "Invalid mobile number")])

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    class Meta:
        app_label = 'ss_users'

    def __str__(self):
        return self.get_fullname()

    def get_fullname(self):
        return self.first_name + " "  \
            + (self.middle_name + " ") if bool(self.middle_name != None \
                    and self.middle_name != "") \
                else  "" + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return True

    @property
    def is_super_user(self):
        return False
