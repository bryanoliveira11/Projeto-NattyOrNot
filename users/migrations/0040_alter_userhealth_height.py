# Generated by Django 4.2.5 on 2024-04-08 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0039_alter_userhealth_height_alter_userhealth_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhealth',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True, verbose_name='Altura (cm)'),
        ),
    ]
