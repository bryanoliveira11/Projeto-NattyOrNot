# Generated by Django 4.2.5 on 2023-10-11 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0009_alter_exercises_created_at'),
        ('users', '0012_alter_usertraining_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Perfil', 'verbose_name_plural': 'Perfis'},
        ),
        migrations.AlterModelOptions(
            name='usertraining',
            options={'verbose_name': 'Treino', 'verbose_name_plural': 'Treinos'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='usertraining',
            name='exercises',
            field=models.ManyToManyField(blank=True, default='', to='training.exercises', verbose_name='Exercícios'),
        ),
        migrations.AlterField(
            model_name='usertraining',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
