# Generated by Django 4.1.4 on 2022-12-24 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_created_on_post_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='user',
            new_name='profile',
        ),
    ]
