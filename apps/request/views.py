from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import telebot
from .models import MemesRequest

bot = telebot.TeleBot(settings.TOKEN)

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@bot.message_handler(commands=['send_meme'])
def handle_send_meme_command(message):
    # проверяем, есть ли в сообщении картинка
    if message.photo:
        # получаем объект картинки
        photo = message.photo[-1]
        # скачиваем файл
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # сохраняем файл
        meme = MemesRequest()
        meme.image.save(f'{file_info.file_unique_id}.jpg', downloaded_file)
        # отправляем сообщение пользователю, что картинка сохранена
        bot.reply_to(message, 'Картинка сохранена')
    else:
        # если картинки нет, отправляем сообщение пользователю
        bot.reply_to(message, 'Пришлите картинку')