from django.core.mail import send_mail

from config import settings


def send_mailing(recipients: list, title: str, text: str) -> None:
    """Отправка рассылки клиентам из списка recipient"""

    send_mail(title,  # Тема письма
              text,
              settings.EMAIL_HOST_USER,  # От кого письмо
              recipient_list=recipients)
