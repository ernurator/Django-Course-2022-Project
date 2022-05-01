# Generated by Django 3.2.12 on 2022-04-30 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_debitcard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('iban', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currency', models.CharField(choices=[('KZT', 'Kazakhstani Tenge'), ('RUR', 'Russian Rubles'), ('USD', 'US Dollars'), ('GBP', 'Great Britain Pounds'), ('EUR', 'Euro')], default='KZT', max_length=3)),
                ('balance', models.PositiveBigIntegerField(default=0)),
                ('rate', models.FloatField()),
                ('due_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', related_query_name='deposit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]