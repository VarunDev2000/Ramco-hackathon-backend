# Generated by Django 3.0.2 on 2020-01-04 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0003_auto_20200104_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='Timestamp',
            field=models.DateTimeField(default=None),
        ),
    ]