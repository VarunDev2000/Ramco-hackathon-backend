# Generated by Django 3.0.2 on 2020-01-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0005_auto_20200104_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Timestamp',
            field=models.DateTimeField(default=None),
        ),
    ]
