from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from users.models import UserProfile

User = get_user_model()


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileDetailClassView(View):
    def get(self, *args, **kwargs):
        user = User.objects.filter(
            username=self.kwargs.get('username')
        ).first()

        # usuário só pode acessar o próprio perfil
        if not user or user != self.request.user:
            raise Http404()

        user_profile = UserProfile.objects.filter(user__id=user.pk).first()

        return render(self.request, 'users/pages/user_profile.html', context={
            'user': user,
            'user_profile': user_profile,
            'title': f'Minha Conta',
        })
