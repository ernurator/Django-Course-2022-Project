import re

from django.contrib.auth.models import AbstractUser, UserManager
from django.core import exceptions
from django.db import models

_PHONE_NUMBER_LENGTH = 12


def _phone_number_validator(value):
    if not re.fullmatch(r'\+\d{11}', value):
        raise exceptions.ValidationError(f'Provided not valid phone number: {value}')


class MerchantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_merchant=True)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_merchant=False)


class User(AbstractUser):
    phone_number = models.CharField(validators=(_phone_number_validator,), max_length=_PHONE_NUMBER_LENGTH,
                                    unique=True, blank=False, null=False)
    is_merchant = models.BooleanField(default=False)

    objects = UserManager()
    merchants = MerchantManager()
    customers = CustomerManager()
