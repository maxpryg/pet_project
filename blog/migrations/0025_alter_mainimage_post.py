# Generated by Django 4.0.5 on 2022-08-11 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_alter_additionalimage_post_alter_mainimage_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainimage',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_main_image', to='blog.post'),
        ),
    ]
