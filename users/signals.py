from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()


@receiver(user_signed_up)
def check_existing_email(sender, request, user, **kwargs):
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
