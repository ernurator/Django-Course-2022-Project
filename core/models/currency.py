from django.db import models

CURRENCY_SYMBOL_LENGTH = 3


class CurrencyEnum(models.TextChoices):
    KZT = 'KZT', 'Kazakhstani Tenge'
    RUR = 'RUR', 'Russian Rubles'
    USD = 'USD', 'US Dollars'
    GBP = 'GBP', 'Great Britain Pounds'
    EUR = 'EUR', 'Euro'
