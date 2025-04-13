from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import UserPassesMixin
from task_manager.user.forms import UserRegistrationForm


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'user/index.html'
    context_object_name = 'users'
# если не указывать, имя переменной в шаблоне
# (по умолчанию: `object_list` ('user_list'))


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Пользователь успешно зарегистрирован'
        )
        return super().form_valid(form)


class UserUpdateView(UserPassesMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('user_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Пользователь успешно изменен'
        )
        return super().form_valid(form)


class UserDeleteView(UserPassesMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_index')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Пользователь успешно удален'
        )
        return super().form_valid(form)
