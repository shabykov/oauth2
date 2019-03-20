from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import mixins
from django.contrib.auth.views import redirect_to_login

from oauth2_provider.models import Application

from ...accounts.mixins import TwoFactorMixin

LoginRequiredMixin = mixins.LoginRequiredMixin
TwoFactorMixin = TwoFactorMixin


class ApplicationPermissionRequiredMixin(mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if self.raise_exception and self.request.user.is_authenticated and not self.request.user.is_superuser:
            return redirect('user_does_not_have_permissions', pk=self.request.user.pk)
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class ApplicationViewMixin(ApplicationPermissionRequiredMixin):
    permission_required = ('oauth2_provider.view_application',)


class ApplicationCreationMixin(ApplicationPermissionRequiredMixin):
    permission_required = ('oauth2_provider.add_application',)


class ModelPermissionRequiredMixin(ApplicationPermissionRequiredMixin):
    def is_from_the_same_application(self):
        application = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif application is not None and isinstance(application, Application):
            return application in self.request.user.get_applications()
        else:
            return False

    def has_permission(self):
        return super().has_permission() and self.is_from_the_same_application()


class ApplicationChangeMixin(ModelPermissionRequiredMixin):
    permission_required = ('oauth2_provider.change_application',)


class ApplicationDeleteMixin(ModelPermissionRequiredMixin):
    permission_required = ('oauth2_provider.delete_application',)
