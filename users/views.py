from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('service:home')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


def activate_new_user(request, pk):
    """Функция для активации нового пользователя"""
    user = get_user_model()  # получение модели пользователя
    user_for_activate = user.objects.get(id=pk)  # получение пользователя с нужным id
    user_for_activate.is_active = True  # смена флага у пользователя на True
    user_for_activate.save()  # сохранение
    return render(request, 'users/activate_user.html')
