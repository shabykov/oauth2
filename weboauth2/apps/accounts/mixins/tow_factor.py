from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from ..models import TwoFactor


class TwoFactorMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.session.get('verified', False):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        if self.request.user.is_authenticated():
            TwoFactor.objects.update_or_create(user=self.request.user)
            self.request.user.two_factor.send_code()
            return reverse_lazy('verify')
        else:
            return reverse_lazy('login')

    def __init__(self, *args, **kwargs):
        super(TwoFactorMixin, self).__init__(*args, **kwargs)
