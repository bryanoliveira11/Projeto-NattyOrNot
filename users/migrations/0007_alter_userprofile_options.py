# Generated by Django 4.2.5 on 2023-09-19 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_userprofile_avatar_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile'},
        ),
    ]
