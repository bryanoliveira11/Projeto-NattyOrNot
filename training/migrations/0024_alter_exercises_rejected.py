# Generated by Django 4.2.5 on 2024-03-07 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0023_alter_exercises_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='rejected',
            field=models.BooleanField(default=False, verbose_name='Rejeitar Exercício (Marque aqui para Rejeitar)'),
        ),
    ]
