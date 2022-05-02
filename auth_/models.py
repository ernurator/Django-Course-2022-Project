import re

from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from django.db import models
# from django.dispatch import receiver

PHONE_NUMBER_LENGTH = 12


def _phone_number_validator(value):
    if not re.fullmatch(r'\+\d{11}', value):
        raise exceptions.ValidationError(f'Provided not valid phone number: {value}')


class User(AbstractUser):
    phone_number = models.CharField(validators=(_phone_number_validator,), max_length=PHONE_NUMBER_LENGTH,
                                    unique=True, blank=False, null=False)
    is_merchant = models.BooleanField(default=False)


# @receiver(models.signals.post_save, sender=User)
# def _update_password(sender, instance, created, **kwargs):
#     if created:
#         instance.set_password(instance.password)
