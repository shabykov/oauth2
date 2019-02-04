from django.urls import reverse_lazy
from django.views import generic
from .. import models, forms, mixins


class UserListView(mixins.UserViewMixin, generic.ListView):
    model = models.User
    context_object_name = 'users'
    template_name = 'user/list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        if self.request.user.is_profile():
            return self.model.objects.filter(profile__applications__in=self.request.user.profile.applications.all())
        return self.model.objects.none()


class UserCreateView(mixins.UserCreationMixin, generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    template_name = 'user/create.html'

    def get_success_url(self):
        return reverse_lazy('user_update', kwargs={'pk': self.object.pk})


class UserUpdateView(mixins.UserChangeMixin, generic.UpdateView):
    model = models.User
    form_class = forms.UserChangeForm
    template_name = 'user/update.html'

    def get_success_url(self):
        return reverse_lazy('users_profile_update', kwargs={'user_pk': self.object.pk, 'pk': self.object.profile.pk})


class UserDeleteView(mixins.UserDeleteMixin, generic.DeleteView):
    model = models.User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
