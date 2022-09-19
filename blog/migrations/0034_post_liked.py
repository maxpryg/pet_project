# Generated by Django 4.0.5 on 2022-09-11 18:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0033_alter_post_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]