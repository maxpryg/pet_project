# Generated by Django 4.0.5 on 2022-07-28 12:45

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_mainimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('image', versatileimagefield.fields.VersatileImageField(upload_to='images/', verbose_name='Image')),
            ],
        ),
    ]
