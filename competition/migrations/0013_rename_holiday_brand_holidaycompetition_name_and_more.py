# Generated by Django 4.2.16 on 2024-10-03 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0012_holidaycompetition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='holidaycompetition',
            old_name='holiday_brand',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='holidaycompetition',
            name='holiday_model',
        ),
    ]
