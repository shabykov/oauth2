from django.urls import reverse_lazy
from django.views import generic

from .. import models, forms


class GroupListView(generic.ListView):
    model = models.Group
    context_object_name = 'groups'
    template_name = 'group/list.html'


class GroupCreateView(generic.CreateView):
    model = models.Group
    form_class = forms.GroupCreationForm
    template_name = 'group/create.html'

    def get_success_url(self):
        return reverse_lazy('group_update', kwargs={'pk': self.object.pk})


class GroupUpdateView(generic.UpdateView):
    model = models.Group
    form_class = forms.GroupChangeForm
    template_name = 'group/update.html'
    success_url = reverse_lazy('group_list')


class GroupDeleteView(generic.DeleteView):
    model = models.Group
    template_name = 'group/delete.html'
    success_url = reverse_lazy('group_list')
