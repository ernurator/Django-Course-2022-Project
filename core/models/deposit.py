import uuid

from django.db import models

from auth_.models import User
from .currency import CurrencyEnum, CURRENCY_SYMBOL_LENGTH


class DepositManager(models.Manager):
    def user_deposits(self, user):
        return self.filter(user=user)


class Deposit(models.Model):
    iban = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(choices=CurrencyEnum.choices, default=CurrencyEnum.KZT,
                                max_length=CURRENCY_SYMBOL_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits', related_query_name='deposit')
    balance = models.FloatField(default=0)
    rate = models.FloatField()
    due_date = models.DateField()

    objects = DepositManager()

    def __str__(self):
        return f'Deposit #{self.iban} of user {self.user}, {self.rate}% rate [{self.balance} {self.currency}]'
