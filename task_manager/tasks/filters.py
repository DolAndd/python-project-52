import django_filters
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from django import forms


class TaskFilter(django_filters.FilterSet):

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        field_name='status',
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        field_name='executor',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["executor"].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    def filter_by_labels(self, queryset, name, value):
        return queryset

    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        field_name='labels',
    )

    self_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
    )

    def filter_self_tasks(self, queryset, name, value):
        if value and hasattr(self, "request"):
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = []


