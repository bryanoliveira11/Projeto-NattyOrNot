import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image

from utils.strings import generate_random_string

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=155, verbose_name='Nome')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Exercises(models.Model):
    title = models.CharField(max_length=155, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descrição')
    slug = models.SlugField(unique=True)
    series = models.IntegerField(verbose_name='Séries')
    reps = models.IntegerField(verbose_name='Repetições')
    is_published = models.BooleanField(default=False, verbose_name='Publicado')
    categories = models.ManyToManyField(
        Categories, blank=True, default='', verbose_name='Categorias'
    )
    published_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Publicado por'
    )
    cover = models.ImageField(
        upload_to='exercises/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name='Imagem / Gif'
    )

    def __str__(self) -> str:
        return self.title

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize(
            (new_width, new_height), Image.LANCZOS
        )

        new_image.save(image_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}{generate_random_string(length=5)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, new_width=840)
            except FileNotFoundError:
                ...

        return saved

    def get_absolute_url(self):
        return reverse('training:exercises_detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'
