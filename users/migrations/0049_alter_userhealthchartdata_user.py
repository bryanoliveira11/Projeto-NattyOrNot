# Generated by Django 4.2.5 on 2024-04-10 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0048_alter_userhealthchartdata_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhealthchartdata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
