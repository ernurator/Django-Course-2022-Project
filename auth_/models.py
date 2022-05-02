import re

from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from django.db import models

PHONE_NUMBER_LENGTH = 12


def _phone_number_validator(value):
    if not re.fullmatch(r'\+\d{11}', value):
        raise exceptions.ValidationError(f'Provided not valid phone number: {value}')


class MerchantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_metrchant=True)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_metrchant=False)


class User(AbstractUser):
    phone_number = models.CharField(validators=(_phone_number_validator,), max_length=PHONE_NUMBER_LENGTH,
                                    unique=True, blank=False, null=False)
    is_merchant = models.BooleanField(default=False)

    merchants = MerchantManager()
    customers = CustomerManager()
