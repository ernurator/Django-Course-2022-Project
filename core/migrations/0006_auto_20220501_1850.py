# Generated by Django 3.2.12 on 2022-05-01 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_debitcard_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='loan',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]
