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
    is_published = models.BooleanField(
        default=False, verbose_name='Exercício Está Publicado'
    )
    shared_status = models.CharField(
        max_length=9, verbose_name='Status de Compartilhamento',
        default='MYSELF', choices=(
            ('MYSELF', 'Somente Você'),
            ('FOLLOWERS', 'Meus Seguidores'),
            ('ALL', 'Todos os Usuários'),
        ))
    was_rejected = models.BooleanField(
        default=False, verbose_name='Exercício Está Rejeitado'
    )
    rejected = models.BooleanField(
        default=False, verbose_name='Rejeitar Exercício'
    )
    extra_info = models.TextField(
        default='',
        blank=True,
        verbose_name='Informações Adicionais de Rejeição'
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
    favorited_by = models.ManyToManyField(
        User, blank=True, default='',
        verbose_name='Favoritado por',
        related_name='favorited_by_users',
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
            'UncheckOneError': 'Desmarque o Publicado ou '
            'o Rejeitar para Continuar.',
            'ExtraInfoError': 'Preencha as Informações Adicionais '
            'antes de Rejeitar.',
            'SharedIsNotAll': 'O Exercício não Está Compartilhado para Todos.',
            'InvalidReject': 'Não é Possível Rejeitar um Exercício '
            'que não esteja Compartilhado para Todos.'
        }

        # validating other data
        if self.is_published and self.rejected:
            errors['is_published'] = messages.get('UncheckOneError')
            errors['rejected'] = messages.get('UncheckOneError')

        if self.is_published and self.was_rejected:
            errors['is_published'] = messages.get('UncheckOneError')
            errors['was_rejected'] = messages.get('UncheckOneError')

        if self.is_published and self.shared_status != 'ALL':
            errors['shared_status'] = messages.get('SharedIsNotAll')

        if self.rejected and not self.extra_info:
            errors['extra_info'] = messages.get('ExtraInfoError')

        if self.rejected and self.shared_status != 'ALL':
            errors['rejected'] = messages.get('InvalidReject')
            errors['shared_status'] = messages.get('InvalidReject')

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
        if self.is_published:
            return reverse(
                'training:exercises_detail', kwargs={"slug": self.slug}
            )

        return reverse('training:home')

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
