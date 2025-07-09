from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First name"), max_length=100, required=True)
    last_name = forms.CharField(
        label=_("Surname"), max_length=100, required=True)
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        required=True,
        help_text=_("Required. Enter a valid email address.")
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "username", "email",
            "password1", "password2"
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(
                pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(
                _("This email address is already in use."))
        return email
