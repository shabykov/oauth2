from django import forms as django_forms

from .. import models


class ProfileCreationForm(django_forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'

    def __init__(self, data=None, **kwargs):
        user = kwargs.pop('user')
        super(ProfileCreationForm, self).__init__(data, **kwargs)
        self.fields['user'].initial = user


class ProfileChangeForm(django_forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'


class UsersProfileChangeForm(ProfileCreationForm):
    pass
