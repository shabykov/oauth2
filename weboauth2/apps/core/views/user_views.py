from django.urls import reverse
from django.views import generic
from .. import models, forms


class UserListView(generic.ListView):
    model = models.User
    context_object_name = 'users'
    template_name = 'user/list.html'

    def get_queryset(self):
        return self.model.objects.all()


class UserCreateView(generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    template_name = 'user/create.html'

    def get_success_url(self):
        return reverse('update_user', kwargs={'pk': self.object.pk})


class UserUpdateView(generic.UpdateView):
    model = models.User
    form_class = forms.UserChangeForm
    template_name = 'user/update.html'

    def get_success_url(self):
        return reverse('update_user', kwargs={'pk': self.object.pk})
