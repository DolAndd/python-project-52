from django.shortcuts import render
from task_manager.statuses.models import Status
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.user.forms import UserRegistrationForm
from task_manager.mixins import UserPassesMixin


# Create your views here.
class StatusIndexView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
# Create your views here.
