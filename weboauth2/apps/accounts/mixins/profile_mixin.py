from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import mixins
from django.contrib.auth.views import redirect_to_login

from ..models import Profile
from .tow_factor import TwoFactorMixin


class ProfilePermissionRequiredMixin(TwoFactorMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect('user_does_not_have_permissions', pk=self.request.user.pk)
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class ProfileViewMixin(ProfilePermissionRequiredMixin):
    permission_required = ('accounts.view_profile',)


class ProfileCreationMixin(ProfilePermissionRequiredMixin):
    permission_required = ('accounts.add_profile',)


class ProfileModelPermissionRequiredMixin(ProfilePermissionRequiredMixin):
    def is_from_the_same_application(self):
        profile = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif profile is not None and isinstance(profile, Profile):
            return self.request.user.is_from_the_same_application(profile.user)
        else:
            return True

    def has_permission(self):
        return super().has_permission() and self.is_from_the_same_application()


class ProfileChangeMixin(ProfileModelPermissionRequiredMixin):
    permission_required = ('accounts.change_profile',)


class ProfileDeleteMixin(ProfileModelPermissionRequiredMixin):
    permission_required = ('accounts.delete_profile',)
