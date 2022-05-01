# Generated by Django 3.2.12 on 2022-04-30 19:09

import core.models.card
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebitCard',
            fields=[
                ('card_number', models.CharField(editable=False, max_length=16, primary_key=True, serialize=False, validators=[core.models.card._card_number_validator])),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='core.bankaccount')),
            ],
        ),
    ]
