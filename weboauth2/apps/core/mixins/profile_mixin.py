from django.urls import reverse_lazy
from django.contrib.auth import mixins


class ProfilePermissionRequiredMixin(mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'


class ProfileCreationMixin(ProfilePermissionRequiredMixin):
    permission_required = ('core.add_profile', 'core.change_profile', 'core.delete_profile', 'core.view_profile',)


class ProfileChangeMixin(ProfilePermissionRequiredMixin):
    permission_required = ('core.change_profile', 'core.delete_profile', 'core.view_profile',)


class ProfileViewMixin(ProfilePermissionRequiredMixin):
    permission_required = ('core.view_profile',)


class ProfileDeleteMixin(ProfilePermissionRequiredMixin):
    permission_required = ('core.delete_profile',)
