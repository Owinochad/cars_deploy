# Generated by Django 5.0.7 on 2024-09-09 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0008_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='car_brand',
            field=models.CharField(default='one', max_length=100),
        ),
    ]
