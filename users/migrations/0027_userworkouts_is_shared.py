# Generated by Django 4.2.5 on 2024-01-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_alter_usernotifications_send_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='userworkouts',
            name='is_shared',
            field=models.BooleanField(default=False),
        ),
    ]
