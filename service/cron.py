from django.core.mail import send_mail

from config import settings
from service.models import MailingLog, Mailing


def send_mailing(recipients: Mailing, title: str, text: str) -> None:
    """Отправка рассылки клиентам из списка recipient"""

    emails = recipients.client.values_list('email')
    for email in emails:
        try:
            send_mail(title,  # Тема письма
                      text,
                      settings.EMAIL_HOST_USER,  # От кого письмо
                      recipient_list=[email])
            status = 'success'
            answer = 'Письмо отправлено успешно!'

        except Exception as err:
            status = 'error'
            answer = str(err)

        MailingLog.objects.create(status=status, answer=answer, mailing=recipients)


def hourly_sending():
    for item in Mailing.objects.filter(periodicity=1):
        item.status = 3
        item.save()
        send_mailing(item)
        item.status = 2
        item.save()


def daily_sending():
    for item in Mailing.objects.filter(periodicity=2):
        item.status = 3
        item.save()
        send_mailing(item)
        item.status = 2
        item.save()


def weekly_sending():
    for item in Mailing.objects.filter(periodicity=3):
        item.status = 3
        item.save()
        send_mailing(item)
        item.status = 2
        item.save()



