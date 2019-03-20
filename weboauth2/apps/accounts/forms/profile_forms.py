from django import forms as django_forms

from .. import models


class ProfileCreationForm(django_forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'

    def __init__(self, data=None, **kwargs):
        user = kwargs.pop('user')
        auth_user = kwargs.pop('auth_user')
        super(ProfileCreationForm, self).__init__(data, **kwargs)

        self.fields['user'].initial = user
        self.fields['user'].queryset = models.User.objects.filter(pk=user.pk)

        if auth_user.is_superuser:
            self.fields['role'].queryset = models.Role.objects.all()
            self.fields['applications'].queryset = models.Application.objects.all()

        elif auth_user.is_profile():
            self.fields['role'].queryset = models.Role.objects.filter(
                id__gte=auth_user.profile.role.id) if auth_user.profile.role is not None else models.Role.objects.none()
            self.fields['applications'].queryset = auth_user.profile.applications.all()

        else:
            self.fields['role'].queryset = models.Role.objects.none()
            self.fields['applications'].queryset = models.Application.objects.none()


class ProfileChangeForm(django_forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'

    def __init__(self, data=None, **kwargs):
        auth_user = kwargs.pop('auth_user')
        super(ProfileChangeForm, self).__init__(data, **kwargs)

        self.fields['user'].initial = self.instance.user
        self.fields['user'].queryset = models.User.objects.filter(pk=self.instance.user.pk)
        if auth_user.is_superuser:
            self.fields['role'].queryset = models.Role.objects.all()
            self.fields['applications'].queryset = models.Application.objects.all()

        elif auth_user.is_profile():
            self.fields['role'].queryset = models.Role.objects.filter(
                id__gte=auth_user.profile.role.id) if auth_user.profile.role is not None else models.Role.objects.none()
            self.fields['applications'].queryset = auth_user.profile.applications.all()

        else:
            self.fields['role'].queryset = models.Role.objects.none()
            self.fields['applications'].queryset = models.Application.objects.none()


class UsersProfileChangeForm(ProfileCreationForm):
    pass
