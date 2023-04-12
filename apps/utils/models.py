from datetime import datetime
from django.db import models, transaction
from django.core.cache import cache


class DeleteManager(models.Manager):
    """
    Объекты не удаляются из БД,
    а помечаются как удаленные и фильтруется только неудаленные
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class CommonFields(models.Model):
    """
    Содержит мета-информацию о наследующих моделях -
    кто создал, когда создал и пометка на удаление
    """

    class Meta:
        abstract = True

    name_ru = models.CharField(
        verbose_name='Название на русском',
        max_length=128,
        null=True, blank=True
    )
    name_en = models.CharField(
        verbose_name='Название на английском',
        max_length=128,
        null=True, blank=True
    )
    name_kk = models.CharField(
        verbose_name='Название на казахском',
        max_length=128,
        null=True, blank=True
    )
    name_kk_lat = models.CharField(
        verbose_name='Название на казахском (латиница)',
        max_length=128,
        null=True, blank=True
    )
    # created_by_user = models.ForeignKey(
    #     'user.User',
    #     verbose_name='Создано пользователем',
    #     related_name='created_%(class)ss',
    #     on_delete=models.DO_NOTHING,
    #     null=True, blank=True
    # )
    created_at = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True,
        editable=False,
        db_index=True,
        null=True,
        blank=True
    )
    # updated_by_user = models.ForeignKey(
    #     'user.User',
    #     verbose_name='Обновлено работником',
    #     related_name='updated_%(class)ss',
    #     on_delete=models.DO_NOTHING,
    #     null=True, blank=True
    # )
    updated_at = models.DateTimeField(
        verbose_name='Обновлено',
        auto_now=True,
        editable=False,
        db_index=True
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        default=False,
        editable=False,
        db_index=True
    )
    #
    # deleted_by_user = models.ForeignKey(
    #     'user.User',
    #     verbose_name='Удалено работником',
    #     related_name='deleted_%(class)ss',
    #     on_delete=models.DO_NOTHING,
    #     null=True, blank=True
    # )
    deleted_at = models.DateTimeField(
        verbose_name='Когда удалена запись',
        editable=False,
        null=True, blank=True
    )

    objects = DeleteManager()

    def delete(self, using=None, keep_parents=False):
        if self.is_deleted:
            return
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    def __str__(self):
        try:
            if hasattr(self, 'name_ru'):
                try:
                    return self.name_ru if self.name_ru else ""
                except:
                    return "нет объекта названия"
            try:
                return super().__str__()
            except (TypeError, AttributeError):
                return "Без названия"
        except:
            return ""

    @transaction.atomic
    def save(self, *args, **kwargs):
        save_data = super().save(*args, **kwargs)
        # print("cache_clear")
        cache.clear()
        return save_data
