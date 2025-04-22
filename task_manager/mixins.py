from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, _("You are not logged in! Please sign in."))
            # Вы не авторизованы! Пожалуйста, выполните вход.
            return redirect('login')
        messages.error(
            self.request, _("You have no rights to change another user"))
        # У вас нет прав для изменения другого пользователя.
        return redirect("user_index")


class UserLoginMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in."))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
