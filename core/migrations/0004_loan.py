# Generated by Django 3.2.12 on 2022-04-30 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_deposit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('KZT', 'Kazakhstani Tenge'), ('RUR', 'Russian Rubles'), ('USD', 'US Dollars'), ('GBP', 'Great Britain Pounds'), ('EUR', 'Euro')], default='KZT', max_length=3)),
                ('balance', models.PositiveBigIntegerField(default=0)),
                ('rate', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', related_query_name='loan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
