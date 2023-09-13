# Generated by Django 4.2.4 on 2023-09-05 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, verbose_name='Titulo')),
                ('description', models.CharField(max_length=250, verbose_name='Descrição')),
                ('cover', models.ImageField(blank=True, default='', upload_to='exercises/%Y/%m/%d/', verbose_name='Imagem/Gif')),
                ('slug', models.SlugField(unique=True)),
                ('series', models.IntegerField()),
                ('reps', models.IntegerField(verbose_name='Repetições')),
                ('is_published', models.BooleanField(default=False, verbose_name='Publicado')),
                ('categories', models.ManyToManyField(blank=True, default='', to='training.categories', verbose_name='Categorias')),
                ('published_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Publicado por')),
            ],
            options={
                'verbose_name': 'Exercício',
                'verbose_name_plural': 'Exercícios',
            },
        ),
    ]
