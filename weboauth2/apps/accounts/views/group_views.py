from django.views import generic
from django.urls import reverse_lazy

from .. import models, forms, mixins


class GroupListView(mixins.TwoFactorMixin, mixins.GroupViewMixin, generic.ListView):
    model = models.Group
    context_object_name = 'groups'
    template_name = 'group/list.html'


class GroupCreateView(mixins.TwoFactorMixin, mixins.GroupCreationMixin, generic.CreateView):
    model = models.Group
    form_class = forms.GroupCreationForm
    template_name = 'group/create.html'

    def get_success_url(self):
        return reverse_lazy('group_update', kwargs={'pk': self.object.pk})


class GroupUpdateView(mixins.TwoFactorMixin, mixins.GroupChangeMixin, generic.UpdateView):
    model = models.Group
    form_class = forms.GroupChangeForm
    template_name = 'group/update.html'
    success_url = reverse_lazy('group_list')


class GroupDeleteView(mixins.TwoFactorMixin, mixins.GroupDeleteMixin, generic.DeleteView):
    model = models.Group
    template_name = 'group/delete.html'
    success_url = reverse_lazy('group_list')
