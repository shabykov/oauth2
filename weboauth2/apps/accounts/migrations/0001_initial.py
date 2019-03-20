# Generated by Django 2.1.7 on 2019-03-20 08:49

import apps.accounts.managers
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='номер телефона')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('patronymic', models.CharField(blank=True, max_length=30, verbose_name='отчество')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting oauth2.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Родитель')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', apps.accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'Администратор'), (2, 'Администратор приложения'), (3, 'Пользователь приложения')], primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('scope', multiselectfield.db.fields.MultiSelectField(choices=[('read', 'чтение'), ('write', 'запись'), ('change', 'изменеие'), ('delete', 'удаление'), ('read+write', 'чтение/запись'), ('read+write+change', 'чтенеие/запись/измение'), ('read+write+change+delete', 'чтенеие/запись/измение/удаление')], default='read+write', max_length=78, verbose_name='Права доступа в приложении')),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='Группы привелегий соотвестующие данной роли')),
            ],
            options={
                'verbose_name': 'роль',
                'verbose_name_plural': 'роли',
            },
        ),
        migrations.CreateModel(
            name='TwoFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.BigIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='two_factor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(help_text='Роль пользователья в системе', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Role', verbose_name='Роль'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]