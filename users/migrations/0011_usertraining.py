# Generated by Django 4.2.5 on 2023-10-11 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_exercises_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0010_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exercises', models.ManyToManyField(blank=True, default='', to='training.exercises', verbose_name='Categorias')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
