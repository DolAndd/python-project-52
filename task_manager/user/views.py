from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.user.forms import UserRegistrationForm


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'user/index.html'
    context_object_name = 'users'
# если не указывать, имя переменной в шаблоне (по умолчанию: `object_list` ('user_list'))


class UserCreate(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "password",]
    template_name = 'user/create.html'
    success_url = '/users/'



