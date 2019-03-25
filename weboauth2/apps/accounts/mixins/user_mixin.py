from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin


from ..models import User
from .tow_factor import TwoFactorMixin


TwoFactorMixin = TwoFactorMixin


class UserPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect('user_does_not_have_permissions', pk=self.request.user.pk)
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class UserViewMixin(UserPermissionRequiredMixin):
    permission_required = ('accounts.view_user',)


class UserCreationMixin(UserPermissionRequiredMixin):
    permission_required = ('accounts.add_user',)


class ModelPermissionRequiredMixin(UserPermissionRequiredMixin):
    def is_from_the_same_application(self):
        user = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif user is not None and isinstance(user, User):
            return self.request.user.is_from_the_same_application(user)
        else:
            return True

    def has_permission(self):
        return super().has_permission() and self.is_from_the_same_application()


class UserChangeMixin(ModelPermissionRequiredMixin):
    permission_required = ('accounts.change_user',)


class UserDeleteMixin(ModelPermissionRequiredMixin):
    permission_required = ('accounts.delete_user',)
