# Generated by Django 4.2.5 on 2023-10-11 19:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_alter_apimediaimages_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercises',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]