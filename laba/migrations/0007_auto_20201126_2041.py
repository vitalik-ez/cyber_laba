# Generated by Django 3.0.2 on 2020-11-26 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0006_auto_20201126_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='windmills',
            name='price_bashta',
        ),
        migrations.AddField(
            model_name='lengthlopati',
            name='price',
            field=models.IntegerField(default=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Ціна'),
        ),
    ]