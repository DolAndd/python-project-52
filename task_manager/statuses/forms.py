from django.forms import ModelForm
from task_manager.statuses.models import Status
from django import forms


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
