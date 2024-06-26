from os import environ
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from dashboard.forms.create_exercise import CreateExerciseForm
from training.models import Exercises
from utils.get_notifications import get_notifications


@method_decorator(  # garantindo que o usuário esteja logado no site
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe base para criação e edição dos forms
class DashboardFormBaseClassView(View):
    def get_exercise(self, id=None):
        exercise = None

        # verificando se há um id na url, se tiver, significa que é uma edição
        if id is not None:
            # validando se foi publicado pelo usuário logado
            exercise = Exercises.objects.filter(
                published_by=self.request.user,
                pk=id,
                is_published=False,
            ).first()

            # lançando erro 404 caso não tenha nenhum resultado para o id
            if not exercise:
                raise Http404()

            # variáveis para controlar título e mensagens ao usuário
            self.title = f'Editar Exercício > {exercise.title}'
            self.is_exercise_edit = True
        else:
            self.title = 'Novo Exercício'
            self.is_exercise_edit = False

        return exercise

    def get_referer_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        path = self.request.path
        create_url = reverse('dashboard:create_exercise')

        if referer is None or path in referer or create_url in referer:
            return reverse('dashboard:user_dashboard')

        return referer

    def render_exercise(self, form):  # renderizando página do form
        notifications, notifications_total = get_notifications(self.request)

        url_to_redirect = self.get_referer_url()

        return render(
            self.request, 'dashboard/pages/create_exercise.html', context={
                'form': form,
                'notifications': notifications,
                'notification_total': notifications_total,
                'title': self.title,
                'captcha_public_key': environ.get('RECAPTCHA_PUBLIC_KEY', ''),
                'captcha_private_key': environ.get(
                    'RECAPTCHA_PRIVATE_KEY', ''
                ),
                'is_exercise_form': True,
                'is_exercise_edit': self.is_exercise_edit,
                'url_to_redirect': url_to_redirect
            })


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# essa mesma classe vai criar e editar exercícios. ID é opcional nos métodos
class DashboardExerciseClassView(DashboardFormBaseClassView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = None

    def get(self, request, id=None):
        exercise = self.get_exercise(id)
        form = CreateExerciseForm(instance=exercise)
        return self.render_exercise(form=form)

    def post(self, request, id=None):
        exercise = self.get_exercise(id)

        form = CreateExerciseForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=exercise
        )

        if form.is_valid():
            exercise = form.save(commit=False)
            # garantindo o usuário que registrou
            exercise.published_by = request.user
            # garantindo que não esteja publicado ainda
            exercise.is_published = False
            # salvando no banco
            exercise.save()
            # garantindo o preenchimento das categorias pós save
            categories = form.cleaned_data.get('categories')

            if categories is not None:
                exercise.categories.set(
                    categories.all()
                )

            if self.is_exercise_edit:
                messages.success(request, 'Exercício Editado com Sucesso !')
            else:
                messages.success(request, 'Exercício Criado com Sucesso !')

            return redirect(reverse(
                'dashboard:edit_exercise', args=(exercise.pk,)
            ))

        return self.render_exercise(form=form)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardDeleteExerciseClassView(DetailView):
    model = Exercises
    template_name = 'users/partials/delete_page.html'
    context_object_name = 'user_exercise'
    pk_url_kwarg = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            pk=self.kwargs.get('id'),
            published_by=self.request.user,
            is_published=False,
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        exercise = context.get('user_exercise')
        title = f'Deletar Exercício - {exercise}'

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercise': exercise,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': title,
            'is_exercise': True,
            'type_of_object': 'Exercício',
            'has_cover': True,
        })
        return context

    def post(self, *args, **kwargs):
        # pegando o exercicio do banco
        exercise_to_delete = self.get_queryset().first()

        # não encontrou no banco
        if not exercise_to_delete:
            messages.error(
                self.request,
                'Um Erro Ocorreu ao Deletar o Exercício.'
            )
            return redirect(reverse('dashboard:user_dashboard'))

        # deletando exercício
        exercise_to_delete.delete()
        messages.success(
            self.request,
            'Exercício Deletado com Sucesso.'
        )

        return redirect(reverse('dashboard:user_dashboard'))
