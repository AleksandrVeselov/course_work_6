from django.urls import path

from service.apps import ServiceConfig
from service.views import home, MailingCreateView, MailingUpdateView, MailingDeleteView, ClientCreateView, \
    MessageCreateView, MailingListView, disable_mailing

app_name = ServiceConfig.name

urlpatterns = [
    path('', home, name='home'),  # Домашняя страница
    path('create/', MailingCreateView.as_view(), name='create'),  # Страница создания рассылки
    path('update/<int:pk>', MailingUpdateView.as_view(), name='update'),  # Страница редактирования рассылки
    path('dalete/<int:pk>', MailingDeleteView.as_view(), name='delete'),  # Страница удаления рассылки
    path('client/create', ClientCreateView.as_view(), name='create_client'),  # Страница создания клиента для рассылки
    path('message/create', MessageCreateView.as_view(), name='create_message'),  # Страница создания сообщения рассылки
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/disable/<int:pk>', disable_mailing, name='disable')
]