from task_manager.tasks.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from task_manager.mixins import UserLoginMixin
from task_manager.tasks.forms import TaskForm
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.
class TaskIndexView(UserLoginMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
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

    def form_valid(self, form):
        messages.success(
            self.request,
            'Задача успешно удалена'
        )
        return super().form_valid(form)


class TaskDetailView(UserLoginMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
