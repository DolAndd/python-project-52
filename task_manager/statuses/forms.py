from django.forms import ModelForm
from task_manager.statuses.models import Status
from django import forms
from django.utils.translation import gettext_lazy as _

class StatusForm(ModelForm):
    name = forms.CharField(label=_("Имя"), max_length=100, required=True)

    class Meta:
        model = Status
        fields = ['name']
