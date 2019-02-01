from django import forms as django_forms

from .. import models


class RoleCreationForm(django_forms.ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'


class RoleChangeForm(django_forms.ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'
