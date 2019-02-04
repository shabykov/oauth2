from django.urls import reverse_lazy
from django.contrib.auth import mixins


class UserPermissionRequiredMixin(mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'


class UserCreationMixin(UserPermissionRequiredMixin):
    permission_required = ('core.add_user', 'core.change_user', 'core.delete_user', 'core.view_user',)


class UserChangeMixin(UserPermissionRequiredMixin):
    permission_required = ('core.change_user', 'core.delete_user', 'core.view_user',)


class UserViewMixin(UserPermissionRequiredMixin):
    permission_required = ('core.view_user',)


class UserDeleteMixin(UserPermissionRequiredMixin):
    permission_required = ('core.delete_user',)
