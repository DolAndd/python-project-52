from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Tasks(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Имя"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_("Статус"))
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_tasks", verbose_name=_("Автор"))
    executor = models.ForeignKey(User, blank=True, on_delete=models.PROTECT, related_name="executed_tasks", verbose_name=_("Исполнитель"))
    # Если у модели несколько связей с одной моделью, related_name обязателен
    labels = models.ManyToManyField(Label, blank=True, verbose_name=_("Метки"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

