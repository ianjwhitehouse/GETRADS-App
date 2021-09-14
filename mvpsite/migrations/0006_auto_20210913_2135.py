# Generated by Django 3.2.4 on 2021-09-14 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvpsite', '0005_auto_20210912_0420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packagead',
            name='receiver_mode',
        ),
        migrations.RemoveField(
            model_name='packagead',
            name='receiver_number',
        ),
        migrations.RemoveField(
            model_name='packagead',
            name='sender_mode',
        ),
        migrations.AddField(
            model_name='courierad',
            name='dep_airport',
            field=models.CharField(default='', max_length=3, verbose_name='Departure airport (3-letter code): '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courierad',
            name='package',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='courierad_package', to='mvpsite.packagead'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='img',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Attach an image: '),
        ),
        migrations.AlterField(
            model_name='courierad',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Still accepting offers'), (1, 'A deal is in progress'), (2, 'A deal is completed'), (3, 'The courier has departed'), (4, 'The courier has arrived'), (7, 'Cancelled'), (8, 'Rated'), (9, 'Attached')], default=0),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='Message body: '),
        ),
        migrations.AlterField(
            model_name='packagead',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Still accepting offers'), (1, 'A deal is in progress'), (2, 'A deal is completed'), (3, 'The package has been dropped off'), (4, 'The package is with the courier'), (5, 'The courier has delivered the package'), (6, 'The package has been received'), (7, 'Cancelled'), (8, 'Rated'), (9, 'Attached')], default=0),
        ),
    ]
