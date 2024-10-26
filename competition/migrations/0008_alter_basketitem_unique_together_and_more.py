# Generated by Django 4.2.16 on 2024-10-23 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_alter_entry_quantity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='basketitem',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='basketitem',
            name='ticket_count',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddConstraint(
            model_name='basketitem',
            constraint=models.UniqueConstraint(condition=models.Q(('competition__isnull', False)), fields=('user', 'competition'), name='unique_user_competition'),
        ),
        migrations.AddConstraint(
            model_name='basketitem',
            constraint=models.UniqueConstraint(condition=models.Q(('holicompetition__isnull', False)), fields=('user', 'holicompetition'), name='unique_user_holicompetition'),
        ),
    ]