from django.contrib import admin

from . import models

admin.site.register([
    models.BankAccount,
    models.DebitCard,
    models.Deposit,
    models.Loan,
])
