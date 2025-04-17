from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переопределяем отображение исполнителя
        self.fields["executor"].label_from_instance = (
            lambda obj: f"{obj.first_name} {obj.last_name}".strip()
                        or obj.username
        )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
