# Generated by Django 4.2.16 on 2024-10-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0011_alter_entry_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='image',
            field=models.ImageField(upload_to='cars'),
        ),
        migrations.AlterField(
            model_name='holidaycompetition',
            name='image',
            field=models.ImageField(upload_to='cars'),
        ),
    ]