from django.core.mail import send_mail

from config import settings
from service import models


def send_mailing(recipients) -> None:
    """Отправка рассылки клиентам из списка recipient"""

    emails = recipients.client.values_list('email')  # список почтовых адресов для рассылки
    title = recipients.message.title  # тема письма
    text = recipients.message.message  # текст письма

    for email in emails:
        try:
            send_mail(title,  # Тема письма
                      text,
                      settings.EMAIL_HOST_USER,  # От кого письмо
                      recipient_list=[email])  # попытка отправить письмо
            status = 'success'
            answer = 'Письмо отправлено успешно!'

        # Если при отправке письма возникает ошибка
        except Exception as err:
            status = 'error'
            answer = str(err)

        models.MailingLog.objects.create(status=status, answer=answer, mailing=recipients)  # создание записи в логе


def hourly_sending():
    """Часовая рассылка"""

    for item in models.Mailing.objects.filter(periodicity=1):
        item.status = 3  # статус запущена
        item.save()  # сохранение
        send_mailing(item)  # отправка письма
        item.status = 2  # статус завершена
        item.save()  # сохранение статуса


def daily_sending():
    """Дневная рассылка"""
    for item in models.Mailing.objects.filter(periodicity=2):
        item.status = 3
        item.save()
        send_mailing(item)
        item.status = 2
        item.save()


def weekly_sending():
    """Недельная рассылка"""
    for item in models.Mailing.objects.filter(periodicity=3):
        item.status = 3
        item.save()
        send_mailing(item)
        item.status = 2
        item.save()



