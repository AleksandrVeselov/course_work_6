
from django.db import models

from service.cron import send_mailing

# варианты периодичности рассылки (раз в день, в неделю, в месяц)
MAILING_PERIODICITY = [(1, 'раз в день'), (2, 'раз в неделю'), (3, 'раз в месяц')]

MAILING_STATUS = [(1, 'завершена'), (2, 'создана'), (3, 'запущена')]  # варианты статуса рассылки
NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class MailingMessage(models.Model):
    """Модель сообщение для рассылки"""

    title = models.CharField(max_length=100, verbose_name='Тема сообщения')  # Тема сообщения
    message = models.TextField(verbose_name='Тело сообщения')  # Тело сообщения

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.title


class Client(models.Model):
    """Модель клиента сервиса рассылок (того кому будем отправлять)"""

    email = models.CharField(max_length=100, verbose_name='Email')  # контактный email
    name = models.CharField(max_length=100, verbose_name='Имя')  # имя
    surname = models.CharField(max_length=100, verbose_name='Фамилия')  # фамилия
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')  # отчество
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)  # комментарий

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    """Модель настройки для рассылки"""

    date_time = models.DateTimeField(verbose_name='Время рассылки')  # время рассылки
    periodicity = models.PositiveSmallIntegerField(choices=MAILING_PERIODICITY, default=1)  # Периодичность
    status = models.PositiveSmallIntegerField(choices=MAILING_STATUS, default=2)  # статус рассылки
    client = models.ManyToManyField(Client)  # клиент рассылки
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE)  # сообщение для рассылки

    def __str__(self):
        return f'Рассылка на {self.date_time} с периодичностью {self.periodicity}. Статус {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    """Модель лог рассылки"""

    date_time = models.DateTimeField(auto_now_add=True)  # дата и время последней попытки (формируется автоматически)
    status = models.CharField(max_length=100, verbose_name='Статус попытки')  # статус попытки
    answer = models.CharField(max_length=100, verbose_name='Ответ сервера', **NULLABLE)  # ответ почтового сервера
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)  # рассылка

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

