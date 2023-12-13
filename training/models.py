from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify

from utils.resize_image import resize_image
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
    slug = models.SlugField(unique=True, blank=True, default='')
    series = models.IntegerField(verbose_name='Séries')
    reps = models.IntegerField(verbose_name='Repetições')
    is_published = models.BooleanField(default=False, verbose_name='Publicado')
    was_rejected = models.BooleanField(
        default=False, verbose_name='Rejeitado Anteriormente (NÃO MEXER)'
    )
    rejected = models.BooleanField(
        default=False, verbose_name='Rejeitar (MARQUE PARA REJEITAR)'
    )
    extra_info = models.TextField(
        default='',
        blank=True,
        verbose_name='Informações Adicionais (em caso de rejeição)'
    )
    categories = models.ManyToManyField(
        Categories, blank=True, default='', verbose_name='Categorias'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em'
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

    def clean(self) -> None:
        clean = super().clean()
        errors = {}
        messages = {
            'UncheckOneError': 'Desmarque o Públicado ou o Rejeitar para Continuar.',
            'ExtraInfoError': 'Preencha as Informações Adicionais antes de Rejeitar.'
        }

        # validating other data
        if self.is_published and self.rejected:
            errors['is_published'] = messages.get('UncheckOneError')
            errors['rejected'] = messages.get('UncheckOneError')

        if self.rejected and not self.extra_info:
            errors['extra_info'] = messages.get('ExtraInfoError')

        if errors:
            raise ValidationError(errors)

        return clean

    def save(self, *args, **kwargs):
        # creating the slug
        if not self.slug:
            slug = f'{slugify(self.title)}{generate_random_string(length=5)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        # resizing the cover image
        if self.cover:
            try:
                resize_image(self.cover, new_width=840)
            except FileNotFoundError:
                ...

        return saved

    def get_absolute_url(self):
        return reverse('training:exercises_detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'


class ApiMediaImages(models.Model):
    name = models.CharField(max_length=155, verbose_name='Nome da Imagem')
    image = models.ImageField(
        upload_to='api/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name='Imagem'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Api Explanation Image'
        verbose_name_plural = 'Api Explanation Images'
