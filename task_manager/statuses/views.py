from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import UserLoginMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


# Create your views here.
class StatusIndexView(UserLoginMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
# Create your views here.


class StatusCreateView(UserLoginMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('status_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Status created successfully")
        )
        # Статус успешно создан
        return super().form_valid(form)


class StatusUpdateView(UserLoginMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('status_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Status changed successfully")
        )
        # Статус успешно изменен
        return super().form_valid(form)


class StatusDeleteView(UserLoginMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('status_index')

    def form_valid(self, form):
        status = self.get_object()
        if status.task_set.exists():  # Проверяем, есть ли связанные задачи
            messages.error(
                self.request,
                _("Cannot delete a status because it is in use")
            )
            # Невозможно удалить статус, потому что он используется
            return redirect('status_index')
        messages.success(
            self.request,
            _("Status removed successfully")
        )
        # Статус успешно удален
        return super().form_valid(form)
