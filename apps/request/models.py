from django.db import models
from apps.utils.models import CommonFields


class MemesRequest(CommonFields):
    message = models.TextField(
        verbose_name='Текст заявки',
        null=True, blank=True)
    image = models.ImageField(
        upload_to='memes',
        verbose_name='Картинка с мемом',
        null=True, blank=True
    )
    sender_id = models.IntegerField(verbose_name='Заявитель', null=True, blank=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Заявка на добавление мема"
        verbose_name_plural = "Заявки на добавление мемов"