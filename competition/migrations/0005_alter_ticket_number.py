# Generated by Django 4.2.16 on 2024-10-23 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_alter_entry_quantity_alter_ticket_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='number',
            field=models.PositiveIntegerField(),
        ),
    ]
