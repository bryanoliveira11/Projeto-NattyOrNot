# Generated by Django 5.1 on 2024-10-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_alter_userhealthchartdata_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userworkouts',
            name='is_shared',
        ),
        migrations.AddField(
            model_name='userworkouts',
            name='shared_status',
            field=models.CharField(choices=[('MYSELF', 'Somente Você'), ('ALL', 'Todos os Usuários')], default='MYSELF', max_length=9, verbose_name='Status de Compartilhamento'),
        ),
    ]
