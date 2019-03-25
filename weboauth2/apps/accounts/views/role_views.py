from django.urls import reverse_lazy
from django.views import generic

from .. import models, forms, mixins


class RoleListView(mixins.TwoFactorMixin, mixins.RoleViewMixin, generic.ListView):
    model = models.Role
    context_object_name = 'roles'
    template_name = 'role/list.html'


class RoleCreateView(mixins.TwoFactorMixin, mixins.RoleCreationMixin, generic.CreateView):
    model = models.Role
    form_class = forms.RoleCreationForm
    template_name = 'role/create.html'

    def get_success_url(self):
        return reverse_lazy('role_update', kwargs={'pk': self.object.pk})


class RoleUpdateView(mixins.TwoFactorMixin, mixins.RoleChangeMixin, generic.UpdateView):
    model = models.Role
    form_class = forms.RoleChangeForm
    template_name = 'role/update.html'
    success_url = reverse_lazy('role_list')


class RoleDeleteView(mixins.TwoFactorMixin, mixins.RoleDeleteMixin, generic.DeleteView):
    model = models.Role
    template_name = 'role/delete.html'
    success_url = reverse_lazy('role_list')
