from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'user/index.html'
    context_object_name = 'users'
# если не указывать, имя переменной в шаблоне (по умолчанию: `object_list` ('user_list'))

class UserCreate(CreateView):
    model = User
    form_class = ArticleForm
    template_name = 'articles/create.html'


class UserUpdate(UpdateView):
    model = User
    form_class = ArticleForm
    template_name = 'articles/update.html'


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('articles:index')
    template_name = 'articles/delete.html'