# Generated by Django 4.2.5 on 2023-11-30 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_usernotifications_subject_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='subject_html',
            field=models.CharField(default='', max_length=255, verbose_name='Assunto HTML'),
        ),
    ]