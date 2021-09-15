# Generated by Django 3.2.4 on 2021-09-14 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvpsite', '0007_auto_20210913_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierad',
            name='package',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courierad_package', to='mvpsite.packagead'),
        ),
        migrations.AlterField(
            model_name='packagead',
            name='courier',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packagead_courier', to='mvpsite.courierad'),
        ),
    ]
