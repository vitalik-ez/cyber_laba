# Generated by Django 3.0.2 on 2020-09-23 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InformKyiv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('number_month', models.PositiveIntegerField()),
                ('UTC', models.TimeField()),
                ('T', models.IntegerField(null=True)),
                ('dd', models.CharField(max_length=30, null=True)),
                ('FF', models.IntegerField(null=True)),
            ],
        ),
    ]