# Generated by Django 5.1.1 on 2024-09-12 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_comment_reply_id_comment_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='post',
        ),
    ]
