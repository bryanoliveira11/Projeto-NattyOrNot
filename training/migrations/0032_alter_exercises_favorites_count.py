# Generated by Django 4.2.5 on 2024-04-04 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0031_alter_exercises_favorites_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='favorites_count',
            field=models.IntegerField(blank=True, default=0, editable=False, verbose_name='Quantidade de Favoritados'),
        ),
    ]
