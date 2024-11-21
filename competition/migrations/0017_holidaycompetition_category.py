# Generated by Django 4.2.16 on 2024-11-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0016_alter_competition_options_remove_competition_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='holidaycompetition',
            name='category',
            field=models.CharField(choices=[('holiday', 'Holiday'), ('electronics', 'Electronics')], default='holiday', help_text='Select the competition category', max_length=20),
        ),
    ]
