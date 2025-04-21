from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.utils.translation import gettext as _

from task_manager.labels.forms import LabelsForm
from task_manager.labels.models import Label
from task_manager.mixins import UserLoginMixin


# Create your views here.
class LabelsIndexView(UserLoginMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
# Create your views here.


class LabelsCreateView(UserLoginMixin, CreateView):
    model = Label
    form_class = LabelsForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('label_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Label created successfully")
        )
        # Метка успешно создана
        return super().form_valid(form)


class LabelsUpdateView(UserLoginMixin, UpdateView):
    model = Label
    form_class = LabelsForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('label_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Label changed successfully")
        )
        # Метка успешно изменена
        return super().form_valid(form)


class LabelsDeleteView(UserLoginMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('label_index')

    def form_valid(self, form):
        label = self.get_object()
        if label.task_set.exists():  # Проверяем, есть ли связанные задачи
            messages.error(
                self.request,
                _("Cannot delete a label because it is in use")
            )
            # Невозможно удалить метку, потому что она используется
            return redirect('label_index')
        messages.success(
            self.request,
            _("Label removed successfully")
        )
        # Метка успешно удалена
        return super().form_valid(form)

