from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from service.forms import MailingForm
from service.models import Mailing, Client, MailingMessage


def home(request):
    """Домашняя страница с выводом списка всех созданных, но не проведенных рассылок"""
    print(request.user.has_perm('service.can_disable_mailings'))
    # если у пользователя есть права
    if request.user.has_perm('service.can_disable_mailings'):
        mailing_list = Mailing.objects.filter(status=2 or 3)  # фильтрация рассылок

    else:
        mailing_list = Mailing.objects.filter(status=2 or 3, owner=request.user.pk)  # фильтрация рассылок

    context = {'object_list': mailing_list, 'title': 'Список активных рассылок'}  # создание контекста для передачи в render
    return render(request, 'service/home.html', context)


class MailingListView(ListView):
    """Класс-представление для вывода всех имеющихся рассылок"""
    model = Mailing
    template_name = 'service/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Список всех рассылок'
        return context
    
    def get_queryset(self):
        """фильтрация всех рассылок, созданных текущим пользователем"""

        # Если у пользователя есть права на отключение любой рассылки
        if self.request.user.has_perm('service.can_disable_mailings'):
            return super().get_queryset()

        # Иначе пользователю доступны только созданные им рассылки
        else:
            return Mailing.objects.filter(owner=self.request.user.pk)


class MailingCreateView(CreateView):
    """Класс-представление для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        mailing = form.save()  # сохранение информации о созданной рассылке
        mailing.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """Класс-представление для редактирования рассылки"""

    model = Mailing
    fields = ('date_time', 'periodicity', 'client', 'status', 'message')
    success_url = reverse_lazy('service:home')


class MailingDeleteView(DeleteView):
    """Класс-представление для удаления рассылки"""

    model = Mailing
    success_url = reverse_lazy('service:home')


class ClientCreateView(CreateView):
    """Класс-представление для создания клиента"""

    model = Client
    success_url = reverse_lazy('service:create')
    fields = ('email', 'name', 'surname', 'patronymic', 'comment')


class MessageCreateView(CreateView):
    """Класс-представление для создания сообщения"""

    model = MailingMessage
    fields = ('title', 'message')
    success_url = reverse_lazy('service:create')


def disable_mailing(request, pk):
    """функция для отключения рассылок"""
    mailing_for_disable = Mailing.objects.get(pk=pk)
    mailing_for_disable.status = 1
    mailing_for_disable.save()
    return redirect(reverse('service:mailings'))