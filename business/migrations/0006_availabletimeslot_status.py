# Generated by Django 5.1.6 on 2025-05-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_alter_availabletimeslot_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabletimeslot',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
