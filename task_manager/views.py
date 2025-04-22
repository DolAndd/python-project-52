from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
