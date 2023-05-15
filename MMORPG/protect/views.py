import random

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import RegisterUserForm, CodeForm, LoginUserForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView
from .models import UserCode
from django.core.mail import send_mail
from .utils import DataMixin


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'protect/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('code')


def LogoutUser(request):
    logout(request)
    return redirect('login')


def s_mail(obj, user):
    send_mail(
        subject='Код подтверждения',
        message=f'{getattr(obj, "code")}',
        from_email='yamargoshka@inbox.ru',
        recipient_list=[User.objects.filter(username=user).values("email")[0]['email']]
    )


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'protect/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        UserCode.objects.create(user=user, code=random.randint(10000, 99999))
        obj = UserCode.objects.get(user=user)
        s_mail(obj, user)
        return redirect('code')


def check_code(request):
    user = request.user
    obj = UserCode.objects.get(user=user)
    if getattr(obj, 'valid'):
        return redirect('/')
    form = CodeForm(request.POST or None)
    error = ''
    if request.method == 'POST':
        if '_check' in request.POST and form.is_valid():
            code2 = form.cleaned_data.get('code', None)
            if UserCode.objects.filter(user=user, code=code2):
                UserCode.objects.filter(user=user).update(valid=True)
                return redirect('/')
            else:
                error = 'Неверный код'
        elif '_send' in request.POST:
            UserCode.objects.filter(user=request.user).update(code=random.randint(10000, 99999))
            s_mail(obj, user)
    context = {'form': form, 'error': error}
    return render(request, 'protect/code.html', context)

class RegisterUserCode(UpdateView):
    template_name = 'protect/code.html'
    form_class = CodeForm
    success_url = '/'

    def get_object(self, **kwargs):
        user = self.request.user
        UserCode.objects.filter(user=self.request.user).update(code=random.randint(10000, 99999))
        q = UserCode.objects.all()
        q = q.values('code', 'code2')[0]
        print(q['code'], q['code2'])
        if q['code'] == q['code2']:
            print('true')
            UserCode.objects.filter(user=self.request.user).update(valid=True)
        send_mail(
            subject=f'Code',
            message=f'{UserCode.objects.filter(user=self.request.user).values("code")}',
            from_email='yamargoshka@inbox.ru',
            recipient_list=[User.objects.filter(username=self.request.user).values("email")[0]['email']]
        )
        return UserCode.objects.get(user=user)