# Generated by Django 4.0.5 on 2022-07-28 11:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 28, 11, 24, 14, 659939, tzinfo=utc)),
        ),
    ]
