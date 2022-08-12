# Generated by Django 4.0.5 on 2022-08-10 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_rename_mainimage_image_delete_additionalimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='additional_images',
        ),
        migrations.RemoveField(
            model_name='post',
            name='main_image',
        ),
        migrations.AddField(
            model_name='image',
            name='main',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]