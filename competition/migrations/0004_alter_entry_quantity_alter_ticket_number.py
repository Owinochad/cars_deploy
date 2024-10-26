# Generated by Django 4.2.16 on 2024-10-22 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_entry_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]