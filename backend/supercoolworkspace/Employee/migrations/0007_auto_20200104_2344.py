# Generated by Django 3.0.2 on 2020-01-04 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0006_auto_20200104_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Timestamp',
            field=models.DateField(default=None),
        ),
    ]