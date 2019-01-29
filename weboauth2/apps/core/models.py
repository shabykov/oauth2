from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.contrib.auth.validators import UnicodeUsernameValidator


from .managers import UserManager


class Role(models.Model):

    ADMIN = 1
    CUSTOMER = 2

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (CUSTOMER, 'customer')
    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        primary_key=True
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы привелегий соотвестующие данной роли'
    )

    def __str__(self):
        return self.get_id_display()

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'роли'


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )

    email = models.EmailField(
        _('email address'),
        unique=True
    )

    phone = models.CharField(
        'номер телефона',
        max_length=12,
        blank=True
    )

    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=True
    )

    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True
    )

    patronymic = models.CharField(
        'отчество',
        max_length=30,
        blank=True
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name='Роль',
        help_text='Роль пользователья, от которого зависит привилегия пользователя'
    )

    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting oauth2.'
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    avatar = models.ImageField(
        upload_to='apps/core/media/avatars/',
        null=True,
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_there_role(self):
        return self.role is not None

    def are_role_groups_empty(self):
        return not self.is_there_role() or self.role.groups.count() == 0

    def set_users_groups_by_role(self):
        """
        Set groups by users role.
        """
        if not self.are_role_groups_empty():
            self.groups.clear()
            self.groups.set(self.role.groups.all())

    def save(self, *args, **kwargs):

        if self.role is not None and self.role == Role.ADMIN:
            self.is_superuser = True

        super(User, self).save(*args, **kwargs)

        self.set_users_groups_by_role()

