# Generated by Django 4.0.5 on 2022-08-04 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_post_additional_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='additional_images',
            field=models.ManyToManyField(blank=True, related_name='additional_images', to='blog.mainimage'),
        ),
        migrations.AlterField(
            model_name='post',
            name='main_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_image', to='blog.mainimage'),
        ),
    ]