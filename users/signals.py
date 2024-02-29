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


def get_user_by_instance(instance):
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
    # updating notification counter
    update_notifications_counter(user=send_to)

    # creating notification in the database
    return UserNotifications.objects.create(
        subject=subj,
        subject_html=subj_html,
        message=msg,
        send_by=send_by,
        send_to=send_to,
    )


def create_profile(user):
    return UserProfile.objects.create(
        user_id=user,
        profile_picture='',
    )


# exercise approved notification
@receiver(post_save, sender=Exercises)
def exercise_published_notification(instance, *args, **kwargs):
    # instance = exercise
    if not instance.is_published:
        return

    # getting user
    user = get_user_by_instance(instance=instance)

    # getting url
    exercise_slug = instance.slug
    msg_url = reverse('training:exercises_detail', args=(exercise_slug,))

    if user:
        create_user_notification(
            subj='Exercício Aprovado',
            subj_html='Exercício' '<p class="green-text m-left"> Aprovado. </p>',
            msg='Seu Exercício '
            f'<a class="notification-url" href="{
                msg_url}">"{instance.title}"</a> '
            'foi <b>Aprovado</b> e está Sendo Exibido na Home.',
            send_to=user,
        )


@receiver(post_save, sender=Exercises)
def exercise_rejected_notification(instance, *args, **kwargs):
    # do nothing if exercise is published = true
    if instance.is_published:
        return

    # rejected = false
    if not instance.rejected:
        return

    user = get_user_by_instance(instance=instance)
    msg_url = reverse('users:edit_exercise', args=(instance.pk,))
    extra_info = instance.extra_info if instance.extra_info else 'Não informado'

    if user:
        create_user_notification(
            subj='Exercício Rejeitado',
            subj_html='Exercício' '<p class="red-text m-left"> Rejeitado. </p>',
            msg='Seu Exercício '
            f'<a class="notification-url" href="{
                msg_url}">"{instance.title}"</a> '
            'foi <b>Rejeitado</b> e não Será Exibido no Site, '
            f'Motivo : {extra_info}.',
            send_to=user,
        )
        ''' setting rejected to be false so the notification will not play again
            if the user tries to edit the exercise.
        '''
        instance.rejected = False
        # checking was rejected so the admin will know it
        instance.was_rejected = True
        instance.save()


# exercise created notification
@receiver(post_save, sender=Exercises)
def exercise_created_notification(instance, created, *args, **kwargs):
    if not created:
        return

    user = get_user_by_instance(instance=instance)
    msg_url = reverse('users:edit_exercise', args=(instance.pk,))

    if user:
        create_user_notification(
            subj='Exercício Criado',
            subj_html='Exercício Criado com Sucesso.',
            msg='Seu Exercício '
            f'<a class="notification-url" href="{
                msg_url}">"{instance.title}"</a> '
            'foi Criado e será Avaliado pela Equipe Administrativa Antes de ser Aprovado.',
            send_to=user,
        )


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
            f'<a class="notification-url" href="{
                msg_url}">{user.username}</a>. '
            'Use os Menus para Navegar no Site. Bons Treinos !',
            send_to=user,
        )


@receiver(user_signed_up)
def configure_google_account(request, user, **kwargs):
    # Verificando se o usuário se inscreveu usando o Google
    google_account = SocialAccount.objects.filter(
        user=user, provider='google'
    ).first()

    if google_account:
        # Pegando o email da conta do Google
        google_account_email = google_account.extra_data.get(  # type:ignore
            'email'
        )

        # criando perfil para o usuário google
        create_profile(user=user.id)

        if google_account_email:
            # Verificar se o email já está em uso
            user_with_email = User.objects.filter(
                email__iexact=google_account_email
            ).exclude(id=user.id).first()

            msg_url = reverse('users:user_profile', args=(user.username,))

            if user_with_email:
                # muda o email para "" caso já exista
                user.email = ""
                user.save()
                messages.warning(
                    request,
                    'Seu E-mail já está associado a outra conta. Mas não se Preocupe, '
                    'é possível editar seus dados '
                    f'<a class="notification-url" href="{
                        msg_url}">Clicando aqui.</a>'
                )
