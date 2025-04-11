import django_filters
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        field_name='status',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Все статусы"
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(is_active=True),
        label='Исполнитель',
        field_name='executor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Любой исполнитель"
    )

    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label='Метки',
        field_name='labels',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = []