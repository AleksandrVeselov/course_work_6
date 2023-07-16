from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from service.models import Mailing, Client, MailingMessage


def home(request):
    """Домашняя страница с выводом списка всех созданных, но не проведенных рассылок"""

    mailing_list = Mailing.objects.filter(status=2 or 3)  # фильтрация рассылок
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


class MailingCreateView(CreateView):
    """Класс-представление для создания рассылки"""
    model = Mailing
    fields = ('date_time', 'periodicity', 'client', 'status', 'message')
    success_url = reverse_lazy('service:home')


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