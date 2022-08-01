# Generated by Django 4.0.5 on 2022-07-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_rename_published_post_blocked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
            ],
        ),
    ]