from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        return redirect("user_index")

