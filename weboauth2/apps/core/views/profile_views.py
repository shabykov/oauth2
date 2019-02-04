import logging

from django.urls import reverse_lazy
from django.views import generic
from .. import models, forms, mixins


class ProfileCreateView(mixins.ProfileCreationMixin, generic.CreateView):
    model = models.Profile
    form_class = forms.ProfileCreationForm
    template_name = 'profile/create.html'

    auth_user = None
    user = None

    def get_initial(self):
        try:
            self.user = models.User.objects.get(pk=self.kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        self.auth_user = self.request.user
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        kwargs['auth_user'] = self.auth_user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile_update', kwargs={'pk': self.object.pk })


class ProfileUpdateView(mixins.ProfileChangeMixin, generic.UpdateView):
    model = models.Profile
    form_class = forms.ProfileChangeForm
    template_name = 'profile/update.html'
    success_url = reverse_lazy('user_list')

    auth_user = None

    def get_initial(self):
        self.auth_user = self.request.user
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['auth_user'] = self.auth_user
        return kwargs


class ProfileDeleteView(mixins.ProfileDeleteMixin, generic.DeleteView):
    model = models.Profile
    template_name = 'profile/delete.html'
    success_url = reverse_lazy('user_list')


class UsersProfileUpdateView(mixins.UserChangeMixin, ProfileUpdateView):
    form_class = forms.UsersProfileChangeForm

    auth_user = None
    user = None

    def get_initial(self):
        try:
            self.user = models.User.objects.get(pk=self.kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        self.auth_user = self.request.user
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        kwargs['auth_user'] = self.auth_user
        return kwargs
