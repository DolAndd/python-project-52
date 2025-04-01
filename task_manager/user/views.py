from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.user.forms import UserRegistrationForm


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'user/index.html'
    context_object_name = 'users'
# если не указывать, имя переменной в шаблоне (по умолчанию: `object_list` ('user_list'))


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/create.html'
    success_url = '/users/'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/update.html'
    success_url = '/users/'


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = '/users/'
