# Generated by Django 4.0.5 on 2022-07-29 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_dashboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
