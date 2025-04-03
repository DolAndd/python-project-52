from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        return redirect("user_index")

