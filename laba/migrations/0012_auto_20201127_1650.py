# Generated by Django 3.0.2 on 2020-11-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0011_auto_20201126_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windmills',
            name='energy_character',
            field=models.FileField(null=True, upload_to='energy_characteristic/'),
        ),
    ]
