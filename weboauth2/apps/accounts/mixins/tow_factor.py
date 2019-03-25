from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import TwoFactor


class TwoFactorMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.session.get('verified', False):
            return self.handle_no_verified()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_verified(self):
        return redirect(self.get_login_url())

    def get_login_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('verify')
        else:
            return reverse_lazy('login')

    def __init__(self, *args, **kwargs):
        super(TwoFactorMixin, self).__init__(*args, **kwargs)
