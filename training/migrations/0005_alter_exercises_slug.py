# Generated by Django 4.2.5 on 2023-10-03 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0004_alter_exercises_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='slug',
            field=models.SlugField(blank=True, default='', unique=True),
        ),
    ]
