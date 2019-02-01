from django import forms as django_forms
from django.contrib.auth import admin, forms

from .. import models


class UserAdmin(admin.UserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'username',
        'email',
        'is_superuser',
    )

    list_filter = ('is_superuser',)

    fieldsets = (
        ('General info', {'fields': ('username', 'email', 'phone', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'patronymic')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff', 'role', 'groups', 'user_permissions',)}),
        ('Meta info', {'fields': ('last_login',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'is_superuser', 'is_active', 'is_staff', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'email',)
    ordering = ('email',)
    filter_horizontal = ()


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ('username', 'email')
        field_classes = {'username': forms.UsernameField, 'email': django_forms.EmailField}


class UserChangeForm(django_forms.ModelForm):
    password = forms.ReadOnlyPasswordHashField(
        label='Пароль',
        help_text='Значение данного поля замаскировано и не отображается в данном поле. '
                  'Вы можете изменить пароль в разделе "Изменить пароль"',
    )

    class Meta:
        model = models.User
        fields = ('username', 'email', 'phone',
                  'last_name', 'first_name', 'patronymic',
                  'is_active', 'is_staff', 'role', 'groups', 'user_permissions')

        field_classes = {'username': forms.UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial.get('password')
