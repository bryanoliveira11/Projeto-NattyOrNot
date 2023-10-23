from os import environ

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from training.models import Exercises
from users.forms import CreateExerciseForm


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
            ).first()

            # lançando erro 404 caso não tenha nenhum resultado para o id
            if not exercise:
                raise Http404()

            # variáveis para controlar título e mensagens ao usuário
            self.title = f'Editar Exercício - {exercise.title}'
            self.is_exercise_edit = True
        else:
            self.title = 'Criar Exercício'
            self.is_exercise_edit = False

        return exercise

    def render_exercise(self, form):  # renderizando página do form
        return render(self.request, 'users/pages/create_exercise.html', context={
            'form': form,
            'search_form_action': reverse('users:user_dashboard_search'),
            'title': self.title,
            'captcha_public_key': environ.get('RECAPTCHA_PUBLIC_KEY', ''),
            'captcha_private_key': environ.get('RECAPTCHA_PRIVATE_KEY', ''),
            'is_exercise_form': True,
            'is_exercise_edit': self.is_exercise_edit,
            'placeholder': 'Pesquise por um Exercício ou Categoria',
            'additional_search_placeholder': 'no Dashboard',
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
        recipe = self.get_exercise(id)
        form = CreateExerciseForm(instance=recipe)
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
            exercise.categories.set(form.cleaned_data.get('categories').all())

            if self.is_exercise_edit:
                messages.success(request, 'Exercício Editado com Sucesso !')
            else:
                messages.success(request, 'Exercício Criado com Sucesso !')

            return redirect(reverse('users:edit_exercise', args=(exercise.pk,)))

        return self.render_exercise(form=form)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardDeleteExerciseClassView(DashboardFormBaseClassView):
    def get(self, *args, **kwargs):
        return redirect(reverse('users:user_dashboard'))

    def post(self, *args, **kwargs):
        exercise = self.get_exercise(self.request.POST.get('id'))

        if exercise:
            messages.success(
                self.request,
                f'Exercício "{exercise.title}" Deletado com Sucesso.'
            )
            exercise.delete()

        return redirect(reverse('users:user_dashboard'))
