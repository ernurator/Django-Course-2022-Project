import re

from django.core import exceptions
from django.db import models

from .account import BankAccount

_CARD_NUMBER_LENGTH = 16


def _card_number_validator(value):
    if not re.fullmatch(r'[4-5]\d{15}', value):
        raise exceptions.ValidationError(f'Provided not valid card number: {value}')


def _prettify_card_number(value):
    return ' '.join(value[i:i + 4] for i in range(0, _CARD_NUMBER_LENGTH, 4))


class DebitCard(models.Model):
    card_number = models.CharField(validators=(_card_number_validator,), max_length=_CARD_NUMBER_LENGTH,
                                   primary_key=True)
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE, related_name='card')

    def __str__(self):
        return f'Card {_prettify_card_number(self.card_number)}'
