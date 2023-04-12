from django.urls import path
from .views import telegram_webhook
from django.conf import settings

urlpatterns = [
    # путь для обработки вебхука от Telegram
    path(f'bot{settings.TOKEN}/', telegram_webhook),

]