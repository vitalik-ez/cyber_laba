# Generated by Django 3.0.2 on 2020-11-09 18:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0002_auto_20200923_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='electricalAppliances',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('power', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.DeleteModel(
            name='Kyiv',
        ),
    ]
