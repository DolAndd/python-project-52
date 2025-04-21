from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name=_("Status"))
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="created_tasks",
                               verbose_name=_("Author"))
    executor = models.ForeignKey(User, blank=True, null=True,
                                 on_delete=models.PROTECT,
                                 related_name="executed_tasks",
                                 verbose_name=_("Executor"))
    # Если у модели несколько связей с одной моделью, related_name обязателен
    labels = models.ManyToManyField(Label, blank=True, verbose_name=_("Labels"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
