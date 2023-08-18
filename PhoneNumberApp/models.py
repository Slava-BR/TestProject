import json

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def authenticate(number):
    try:
        user = CustomUser.objects.get(phone_number=number)
        return user
    except CustomUser.DoesNotExist:
        return None


class CustomUser(AbstractBaseUser):
    password = models.CharField(_("password"),
                                max_length=128,
                                blank=True,
                                null=True)
    phone_number = PhoneNumberField(unique=True, verbose_name='phone number')
    invite_code = models.CharField(max_length=6,
                                   validators=[RegexValidator(regex='[\dA-Za-z]{6}')],
                                   unique=True)
    invitation_code = models.ForeignKey('self',
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        related_name='custom_user')

    def __str__(self):
        return self.invite_code

