from django.db import models

from auth_.models import User
from .currency import CurrencyEnum, CURRENCY_SYMBOL_LENGTH


class Loan(models.Model):
    currency = models.CharField(choices=CurrencyEnum.choices, default=CurrencyEnum.KZT,
                                max_length=CURRENCY_SYMBOL_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans', related_query_name='loan')
    balance = models.PositiveBigIntegerField(default=0)
    rate = models.FloatField()

    def __str__(self):
        return f'Loan({self.balance} {self.currency}) for {self.user} with {self.rate}% rate'
