# Generated by Django 4.1.5 on 2023-02-24 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomLink',
            new_name='Report',
        ),
    ]