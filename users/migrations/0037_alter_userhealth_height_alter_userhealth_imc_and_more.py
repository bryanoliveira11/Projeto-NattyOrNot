# Generated by Django 4.2.5 on 2024-04-08 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_userhealth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhealth',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Altura'),
        ),
        migrations.AlterField(
            model_name='userhealth',
            name='imc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='IMC'),
        ),
        migrations.AlterField(
            model_name='userhealth',
            name='protein_intake',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Proteína Recomendada (g)'),
        ),
        migrations.AlterField(
            model_name='userhealth',
            name='water_intake',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Aguá Recomendada (ml)'),
        ),
        migrations.AlterField(
            model_name='userhealth',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Peso'),
        ),
    ]