# Generated by Django 2.0.9 on 2019-03-22 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
