# Generated by Django 4.2.5 on 2023-11-30 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_usernotifications_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotifications',
            name='subject_html',
            field=models.CharField(default='', max_length=255, verbose_name='Assunto'),
        ),
    ]