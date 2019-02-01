import logging

from django.urls import reverse_lazy
from django.views import generic
from .. import models, forms


class ProfileCreateView(generic.CreateView):
    model = models.Profile
    form_class = forms.ProfileCreationForm
    template_name = 'profile/create.html'
    user = None

    def get(self, request, *args, **kwargs):
        try:
            self.user = models.User.objects.get(pk=kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        return super(ProfileCreateView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile_update', kwargs={'pk': self.object.pk })


class ProfileUpdateView(generic.UpdateView):
    model = models.Profile
    form_class = forms.ProfileChangeForm
    template_name = 'profile/update.html'
    success_url = reverse_lazy('user_list')


class ProfileDeleteView(generic.DeleteView):
    model = models.Profile
    template_name = 'profile/delete.html'
    success_url = reverse_lazy('user_list')


class UsersProfileUpdateView(ProfileUpdateView):
    form_class = forms.UsersProfileChangeForm
    user = None

    def get(self, request, *args, **kwargs):
        try:
            self.user = models.User.objects.get(pk=kwargs['user_pk'])
        except Exception as error:
            logging.error(str(error))
        return super(UsersProfileUpdateView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs
