import logging

from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .. import models, forms, mixins


class UserListView(mixins.TwoFactorMixin, mixins.UserViewMixin, generic.ListView):
    model = models.User
    context_object_name = 'users'
    template_name = 'user/list.html'
    auth_user = None

    def get_queryset(self):
        self.auth_user = self.request.user

        if self.auth_user.is_superuser:
            return self.model.objects.all()

        if self.auth_user.is_profile():
            return self.model.objects.filter(
                Q(pk=self.auth_user.pk) | Q(parent=self.auth_user),
                profile__applications__in=self.auth_user.profile.applications.all())

        return self.model.objects.none()


class UserCreateView(mixins.TwoFactorMixin, mixins.UserCreationMixin, generic.CreateView):
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


class UserUpdateView(mixins.TwoFactorMixin, mixins.UserChangeMixin, generic.UpdateView):
    model = models.User
    form_class = forms.UserChangeForm
    template_name = 'user/update.html'
    auth_user = None

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['auth_user'] = self.auth_user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('users_profile_update', kwargs={'user_pk': self.object.pk, 'pk': self.object.profile.pk})

    def get_queryset(self):
        self.auth_user = self.request.user

        if self.auth_user.is_superuser:
            return self.model.objects.all()

        if self.auth_user.is_profile():
            return self.model.objects.filter(Q(pk=self.auth_user.pk) | Q(parent=self.auth_user))

        return self.model.objects.none()


class UserDeleteView(mixins.TwoFactorMixin, mixins.UserDeleteMixin, generic.DeleteView):
    model = models.User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')


class UserDetailView(mixins.TwoFactorMixin, mixins.UserViewMixin, generic.DetailView):
    model = models.User
    template_name = 'user/detail.html'


class UserDoesNotHavePermissionsView(mixins.TwoFactorMixin, generic.TemplateView):
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
