from django.urls import reverse_lazy
from django.contrib.auth import mixins


class RolePermissionRequiredMixin(mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'


class RoleCreationMixin(RolePermissionRequiredMixin):
    permission_required = ('core.add_role', 'core.change_role', 'core.delete_role', 'core.view_role',)


class RoleChangeMixin(RolePermissionRequiredMixin):
    permission_required = ('core.change_role', 'core.delete_role', 'core.view_role',)


class RoleViewMixin(RolePermissionRequiredMixin):
    permission_required = ('core.view_role',)


class RoleDeleteMixin(RolePermissionRequiredMixin):
    permission_required = ('core.delete_role',)
