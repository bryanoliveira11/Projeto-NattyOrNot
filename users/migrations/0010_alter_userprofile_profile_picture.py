# Generated by Django 4.2.5 on 2023-09-19 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userprofile_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='', upload_to='users/%Y/%m/%d/', verbose_name='Foto de Perfil'),
        ),
    ]