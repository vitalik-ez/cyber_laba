# Generated by Django 3.0.2 on 2020-11-28 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0017_auto_20201128_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tower',
            name='windmills',
            field=models.IntegerField(),
        ),
    ]
