# Generated by Django 4.0.5 on 2022-09-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_customuser_birth_date_alter_customuser_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(max_length=30),
        ),
    ]
