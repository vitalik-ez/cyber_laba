# Generated by Django 3.0.2 on 2020-11-26 18:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0008_auto_20201126_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lengthlopati',
            name='price',
            field=models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Ціна'),
        ),
    ]
