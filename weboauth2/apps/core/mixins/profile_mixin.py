from django.urls import reverse_lazy
from django.contrib.auth import mixins

from ..models import Profile


class ProfilePermissionRequiredMixin(mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'


class ProfileViewMixin(ProfilePermissionRequiredMixin):
    permission_required = ('core.view_profile',)


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


class ProfileCreationMixin(ProfileModelPermissionRequiredMixin):
    permission_required = ('core.add_profile', 'core.change_profile', 'core.delete_profile', 'core.view_profile',)


class ProfileChangeMixin(ProfileModelPermissionRequiredMixin):
    permission_required = ('core.change_profile', 'core.delete_profile', 'core.view_profile',)


class ProfileDeleteMixin(ProfileModelPermissionRequiredMixin):
    permission_required = ('core.delete_profile',)
