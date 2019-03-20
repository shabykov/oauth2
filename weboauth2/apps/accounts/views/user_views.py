import logging

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .. import models, forms, mixins


class UserListView(mixins.ApplicationOwnerIsUserMixin, mixins.UserViewMixin, generic.ListView):
    model = models.User
    context_object_name = 'users'
    template_name = 'user/list.html'


class UserCreateView(mixins.UserCreationMixin, generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    template_name = 'user/create.html'

    def get_success_url(self):
        return reverse_lazy('user_update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.parent = self.request.user
        self.object.save()
        return super().form_valid(form)


class UserUpdateView(mixins.UserOwnerIsUserMixin, mixins.UserChangeMixin, generic.UpdateView):
    model = models.User
    form_class = forms.UserChangeForm
    template_name = 'user/update.html'

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['auth_user'] = self.auth_user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('users_profile_update', kwargs={'user_pk': self.object.pk, 'pk': self.object.profile.pk})


class UserDeleteView(mixins.UserDeleteMixin, generic.DeleteView):
    model = models.User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')


class UserDetailView(mixins.UserViewMixin, generic.DetailView):
    model = models.User
    template_name = 'user/detail.html'


class UserDoesNotHavePermissionsView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/does_not_have_permissions.html'
    user = None

    def get(self, request, *args, **kwargs):
        try:
            self.user = get_object_or_404(models.User, pk=kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        return super(UserDoesNotHavePermissionsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDoesNotHavePermissionsView, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context
