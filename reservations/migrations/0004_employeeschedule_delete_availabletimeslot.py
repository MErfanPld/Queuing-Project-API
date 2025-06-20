# Generated by Django 5.1.6 on 2025-05-26 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_business_business_type'),
        ('reservations', '0003_availabletimeslot_delete_availabletime'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(0, 'دوشنبه'), (1, 'سه\u200cشنبه'), (2, 'چهارشنبه'), (3, 'پنجشنبه'), (4, 'جمعه'), (5, 'شنبه'), (6, 'یک\u200cشنبه')], verbose_name='روز هفته')),
                ('time', models.TimeField(verbose_name='ساعت')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='business.employee', verbose_name='کارمند')),
            ],
            options={
                'verbose_name': 'برنامه کاری',
                'verbose_name_plural': 'برنامه\u200cهای کاری',
                'unique_together': {('employee', 'weekday', 'time')},
            },
        ),
        migrations.DeleteModel(
            name='AvailableTimeSlot',
        ),
    ]
