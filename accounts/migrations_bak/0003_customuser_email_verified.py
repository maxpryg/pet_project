# Generated by Django 4.0.5 on 2022-07-26 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_birth_date_customuser_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]