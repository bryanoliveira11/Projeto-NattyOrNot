# Generated by Django 4.2.5 on 2023-12-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0016_alter_exercises_was_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='was_rejected',
            field=models.BooleanField(default=False, verbose_name='Rejeitado Anteriormente (NÃO MEXER)'),
        ),
    ]
