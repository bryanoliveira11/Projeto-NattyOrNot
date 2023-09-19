from django.contrib.auth.models import User
from django.db import models

from utils.resize_image import resize_image


class UserProfile(models.Model):
    # se o usuário for deletado, o perfil também será
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name='Foto de Perfil'
    )

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.profile_picture:
            try:
                resize_image(self.profile_picture, new_width=600)
            except FileNotFoundError:
                ...

        return saved
