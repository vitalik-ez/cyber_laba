# Generated by Django 3.0.2 on 2020-11-28 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0016_auto_20201128_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tower',
            name='windmills',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laba.Windmills'),
        ),
    ]