# Generated by Django 4.0.5 on 2022-08-04 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_post_additional_images_alter_post_main_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MainImage',
            new_name='Image',
        ),
        migrations.DeleteModel(
            name='AdditionalImage',
        ),
    ]
