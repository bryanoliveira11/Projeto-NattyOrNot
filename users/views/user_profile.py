from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

User = get_user_model()


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileDetailClassView(View):
    def get(self, *args, **kwargs):
        user = User.objects.filter(pk=self.kwargs.get('id')).first()

        if not user:
            raise Http404()

        return render(self.request, 'users/pages/user_profile.html', context={
            'user': user,
            'title': f'Minha Conta',
        })
