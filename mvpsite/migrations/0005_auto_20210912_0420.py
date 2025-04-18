# Generated by Django 3.2.4 on 2021-09-12 08:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvpsite', '0004_auto_20210912_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='seen',
        ),
        migrations.AddField(
            model_name='message',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='regarding_code',
            field=models.SmallIntegerField(choices=[(1, 'Courier Ad'), (2, 'Package Ad')]),
        ),
        migrations.AlterField(
            model_name='packagead',
            name='receiver_number',
            field=models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone number for pickup: '),
        ),
        migrations.AlterField(
            model_name='profile',
            name='num_of_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.FloatField(default=5),
        ),
    ]
