from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True) # по умолчанию необязательное поле
    last_name = forms.CharField(max_length=100, required=True) # по умолчанию необязательное поле
    class Meta:
        model = User
        fields = [ "username",  "first_name", "last_name",  "password1", "password2",]
