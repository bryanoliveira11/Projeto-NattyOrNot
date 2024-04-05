from django.contrib.auth import get_user_model
from django.db import models

from training.models import Exercises
from utils.resize_image import resize_image

User = get_user_model()


class UserProfile(models.Model):
    # se o usuário for deletado, o perfil também será
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Usuário',
        blank=True,
    )
    profile_picture = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name='Foto de Perfil'
    )
    biography = models.TextField(
        verbose_name='Biografia', default='', null=True, blank=True
    )
    notifications_total = models.IntegerField(
        null=False,
        default=0,
        verbose_name='Notificações não Vistas',
        editable=False,
    )
    forgot_password_code = models.CharField(
        max_length=6,
        blank=True,
        default='',
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em'
    )

    def __str__(self) -> str:
        return self.user.get_username()

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.profile_picture:
            try:
                resize_image(self.profile_picture, new_width=600)
            except FileNotFoundError:
                ...

        return saved

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


class UserWorkouts(models.Model):
    title = models.CharField(
        max_length=155, verbose_name='Nome do Treino', default=''
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        blank=True,
    )
    exercises = models.ManyToManyField(
        Exercises, blank=True, default='',
        verbose_name='Exercícios',
        limit_choices_to={'is_published': True}
    )
    exercises_total = models.IntegerField(
        default=0, verbose_name='Total de Exercícios'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )
    is_shared = models.BooleanField(
        default=False, verbose_name='Compartilhado'
    )

    def __str__(self) -> str:
        return f'Treino de {self.user.get_username()}'

    class Meta:
        verbose_name = 'Treino'
        verbose_name_plural = 'Treinos'


class UserNotifications(models.Model):
    subject = models.CharField(
        max_length=155, verbose_name='Assunto', default=''
    )
    subject_html = models.CharField(
        max_length=255, verbose_name='Assunto HTML', default=''
    )
    message = models.TextField(verbose_name='Mensagem')
    send_by = models.CharField(max_length=155, verbose_name='Enviado por')
    send_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Enviado para'
    )
    send_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Enviado em'
    )

    def __str__(self) -> str:
        return f'Notificação de {self.send_to.get_username()}'

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
