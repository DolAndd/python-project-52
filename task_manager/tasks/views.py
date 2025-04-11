from task_manager.tasks.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from task_manager.mixins import UserLoginMixin
from task_manager.tasks.forms import TaskForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django_filters.views import FilterView
from .filters import TaskFilter


# Create your views here.
class TaskIndexView(UserLoginMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('status', 'executor', 'author').prefetch_related('labels')
# Create your views here.


class TaskCreateView(UserLoginMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('task_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            'Задача успешно создана'
        )
        return super().form_valid(form)


class TaskUpdateView(UserLoginMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('task_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Задача успешно изменена'
        )
        return super().form_valid(form)


class TaskDeleteView(UserLoginMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('task_index')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверяем, является ли текущий пользователь автором задачи
        if self.object.author != request.user:
            messages.error(
                self.request,
                'Задачу может удалить только ее автор'
            )
            return redirect('task_index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            'Задача успешно удалена'
        )
        return super().form_valid(form)


class TaskDetailView(UserLoginMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
