from django.urls import reverse_lazy
from django.contrib.auth import mixins


class GroupPermissionRequiredMixin(mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'


class GroupCreationMixin(GroupPermissionRequiredMixin):
    permission_required = ('core.add_group', 'core.change_group', 'core.delete_group', 'core.view_group',)


class GroupChangeMixin(GroupPermissionRequiredMixin):
    permission_required = ('core.change_group', 'core.delete_group', 'core.view_group',)


class GroupViewMixin(GroupPermissionRequiredMixin):
    permission_required = ('core.view_group',)


class GroupDeleteMixin(GroupPermissionRequiredMixin):
    permission_required = ('core.delete_group',)
