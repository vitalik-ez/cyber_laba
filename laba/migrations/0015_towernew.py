# Generated by Django 3.0.2 on 2020-11-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laba', '0014_auto_20201128_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='TowerNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(verbose_name='Висота new башти')),
                ('price', models.IntegerField(verbose_name='Вартість new башти')),
                ('windmills', models.IntegerField(verbose_name='Який вітряк')),
            ],
        ),
    ]
