# Generated by Django 5.0.3 on 2024-09-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_competitionimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesatransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='mpesatransaction',
            name='mpesa_receipt_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mpesatransaction',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mpesatransaction',
            name='transaction_date',
            field=models.DateTimeField(null=True),
        ),
    ]