# Generated by Django 4.0.5 on 2022-08-11 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_alter_mainimage_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainimage',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_image', to='blog.post'),
        ),
    ]
