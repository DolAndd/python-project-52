from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    # verbose_name указывает название поля в шаблоне.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
