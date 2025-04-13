from django.forms import ModelForm

from task_manager.labels.models import Label


class LabelsForm(ModelForm):

    class Meta:
        model = Label
        fields = ['name']
