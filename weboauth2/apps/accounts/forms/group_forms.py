from django import forms as django_forms

from .. import models


class GroupCreationForm(django_forms.ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'


class GroupChangeForm(django_forms.ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'
