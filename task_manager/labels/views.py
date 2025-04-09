from task_manager.labels.models import Label
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import UserLoginMixin
from task_manager.labels.forms import LabelsForm
from django.contrib import messages
from django.urls import reverse_lazy


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
            'Метка успешно создана'
        )
        return super().form_valid(form)


class LabelsUpdateView(UserLoginMixin, UpdateView):
    model = Label
    form_class = LabelsForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('label_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Метка успешно изменена'
        )
        return super().form_valid(form)


class LabelsDeleteView(UserLoginMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('label_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Метка успешно удалена'
        )
        return super().form_valid(form)

