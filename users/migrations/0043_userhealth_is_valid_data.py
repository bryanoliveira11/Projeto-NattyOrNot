# Generated by Django 4.2.5 on 2024-04-08 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_alter_userhealth_imc_alter_userhealth_protein_intake_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhealth',
            name='is_valid_data',
            field=models.BooleanField(default=False),
        ),
    ]
