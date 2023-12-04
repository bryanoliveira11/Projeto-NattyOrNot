from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from training.models import Exercises
from users.models import UserNotifications, UserProfile

User = get_user_model()


def get_user_data(instance):
    if not instance:
        return

    user = instance.published_by
    return user


def update_notifications_counter(user):
    user_profile = UserProfile.objects.filter(user_id=user).first()

    if not user_profile:
        return

    user_profile.notifications_total += 1
    user_profile.save()


def create_user_notification(subj, subj_html, msg, send_to, send_by='NattyOrNot'):
    return UserNotifications.objects.create(
        subject=subj,
        subject_html=subj_html,
        message=msg,
        send_by=send_by,
        send_to=send_to,
    )


# exercise approved notification
@receiver(post_save, sender=Exercises)
def exercise_published_notification(instance, *args, **kwargs):
    # instance = exercise
    if not instance.is_published:
        return

    # getting user
    user = get_user_data(instance=instance)

    # getting url
    exercise_slug = instance.slug
    msg_url = reverse('training:exercises_detail', args=(exercise_slug,))

    if user:
        create_user_notification(
            subj='Exercício Aprovado',
            subj_html='Exercício' '<p class="green-text m-left"> Aprovado. </p>',
            msg='Seu Exercício '
            f'<a class="notification-url" href="{msg_url}">"{instance.title}"</a> '
            'foi Aprovado e está Sendo Exibido na Home.',
            send_to=user,
        )

    update_notifications_counter(user)


# exercise created notification
@receiver(post_save, sender=Exercises)
def exercise_created_notification(instance, created, *args, **kwargs):
    if not created:
        return

    user = get_user_data(instance=instance)
    msg_url = reverse('users:edit_exercise', args=(instance.pk,))

    if user:
        create_user_notification(
            subj='Exercício Criado',
            subj_html='Exercício Criado com Sucesso.',
            msg='Seu Exercício '
            f'<a class="notification-url" href="{msg_url}">"{instance.title}"</a> '
            'foi Criado e será Avaliado pela Equipe Administrativa Antes de ser Aprovado.',
            send_to=user,
        )

    update_notifications_counter(user)


# user signin notification
@receiver(post_save, sender=User)
def user_signin_notification(instance, created, *args, **kwargs):
    if not created:
        return

    user = instance
    msg_url = reverse('users:user_profile', args=(user.username,))
    subj = 'Boas-Vindas !'

    if user:
        create_user_notification(
            subj=subj,
            subj_html=subj,
            msg='Bem Vindo ao NattyOrNot '
            f'<a class="notification-url" href="{msg_url}">{user.username}</a> ! '
            'Use o Menu Lateral ou o Menu Rápido Abaixo da Barra de Pesquisa '
            'para Navegar no Site. Bons Treinos !',
            send_to=user,
        )

    update_notifications_counter(user)


@receiver(user_signed_up)
def check_existing_email(request, user, **kwargs):
    # Verifique se o usuário se inscreveu usando o Google
    google_account = SocialAccount.objects.filter(
        user=user, provider='google'
    ).first()

    if google_account:
        # Pegando o email da conta do Google
        google_account_email = google_account.extra_data.get(  # type:ignore
            'email'
        )

        if google_account_email:
            # Verificar se o email já está em uso
            user_with_email = User.objects.filter(
                email__iexact=google_account_email
            ).exclude(id=user.id).first()

            if user_with_email:
                # muda o email para "" caso já exista
                user.email = ""
                user.save()
                messages.warning(
                    request,
                    'Seu E-mail já está associado a outra conta. Mas não se Preocupe, '
                    'é possível editar seus dados em " Menu > Meu Perfil ".'
                )
