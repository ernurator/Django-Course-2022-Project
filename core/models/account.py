import uuid

from django.db import models

from auth_.models import User
from .currency import CurrencyEnum, CURRENCY_SYMBOL_LENGTH


class BankAccount(models.Model):
    iban = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(choices=CurrencyEnum.choices, default=CurrencyEnum.KZT,
                                max_length=CURRENCY_SYMBOL_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts', related_query_name='account')
    balance = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'Account #{self.iban} of user {self.user}'
