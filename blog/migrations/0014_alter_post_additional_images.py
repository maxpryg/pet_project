# Generated by Django 4.0.5 on 2022-08-02 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_post_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='additional_images',
            field=models.ManyToManyField(blank=True, to='blog.additionalimage'),
        ),
    ]
