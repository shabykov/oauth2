from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import mixins
from django.contrib.auth.views import redirect_to_login


from ...accounts.mixins import TwoFactorMixin

LoginRequiredMixin = mixins.LoginRequiredMixin


class AuthRequiredMixin(TwoFactorMixin):
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect('user_does_not_have_permissions', pk=self.request.user.pk)
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
