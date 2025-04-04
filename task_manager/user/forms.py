from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_("Имя"), max_length=100, required=True)
    # по умолчанию необязательное поле, добавляем как обязательное
    last_name = forms.CharField(label=_("Фамилия"), max_length=100, required=True)
    # label=_("Имя") указываем для перевода на русский язык в шаблоне

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data['username']
        # Исключаем текущего пользователя из проверки в случае редактирования пользователя
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        # выдает ошибку в случае создания нового пользователя с таким же username
        return username
