# Generated by Django 5.1.6 on 2025-02-18 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='تصویر'),
        ),
    ]
