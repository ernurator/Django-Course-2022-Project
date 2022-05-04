import uuid

from django.db import models

from auth_.models import User
from .currency import CurrencyEnum, CURRENCY_SYMBOL_LENGTH


class BankAccountManager(models.Manager):
    def user_accounts(self, user):
        return self.filter(user=user)

    def get_user_account(self, user, iban):
        return self.user_accounts(user).filter(iban=iban).first()


class BankAccount(models.Model):
    iban = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(choices=CurrencyEnum.choices, default=CurrencyEnum.KZT,
                                max_length=CURRENCY_SYMBOL_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts', related_query_name='account')
    balance = models.FloatField(default=0)

    objects = BankAccountManager()

    def __str__(self):
        return f'Account #{self.iban} of user {self.user}'
