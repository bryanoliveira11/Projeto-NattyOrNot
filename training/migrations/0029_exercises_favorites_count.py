# Generated by Django 4.2.5 on 2024-03-23 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0028_alter_exercises_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercises',
            name='favorites_count',
            field=models.IntegerField(blank=True, default=0, editable=False),
        ),
    ]
