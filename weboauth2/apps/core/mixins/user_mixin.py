from django.urls import reverse_lazy
from django.contrib.auth import mixins

from ..models import User


class UserPermissionRequiredMixin(mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'


class UserViewMixin(UserPermissionRequiredMixin):
    permission_required = ('core.view_user',)


class UserModelPermissionRequiredMixin(UserPermissionRequiredMixin):
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


class UserCreationMixin(UserModelPermissionRequiredMixin):
    permission_required = ('core.add_user', 'core.change_user', 'core.delete_user', 'core.view_user',)


class UserChangeMixin(UserModelPermissionRequiredMixin):
    permission_required = ('core.change_user', 'core.delete_user', 'core.view_user',)

    def has_permission(self):
        return super().has_permission() and self.is_from_the_same_application()


class UserDeleteMixin(UserModelPermissionRequiredMixin):
    permission_required = ('core.delete_user',)
