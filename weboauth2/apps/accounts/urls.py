from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),

    #  login, logout views
    url(
        r'^accounts/login/$',
        views.LoginView.as_view(),
        name='login'
    ),
    url(
        r'^accounts/send-new/$',
        views.TwoFactorSendNewView.as_view(),
        name='send_new_code'
    ),
    url(
        r'^accounts/verify/$',
        views.TwoFactorVerifyView.as_view(),
        name='verify'
    ),
    url(
        r'^accounts/logout/$',
        LogoutView.as_view(),
        name='logout'
    ),

    # password reset views
    url(
        r'^accounts/password-reset/$',
        views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        r'^accounts/reset/done/$',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    url(
        r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(
        r'^accounts/password-reset/complete/$',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    # password change views
    url(
        r'^accounts/password-change/$',
        views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    url(
        r'^accounts/password-change/done/$',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    # Users views
    url(
        r'^users/$',
        views.UserListView.as_view(),
        name='user_list'
    ),
    url(
        r'^users/add/$',
        views.UserCreateView.as_view(),
        name='user_create'
    ),
    url(
        r'^users/(?P<pk>\d+)/update/$',
        views.UserUpdateView.as_view(),
        name='user_update'
    ),
    url(
        r'^users/(?P<pk>\d+)/delete/$',
        views.UserDeleteView.as_view(),
        name='user_delete'
    ),
    url(
        r'^users/(?P<pk>\d+)/detail/$',
        views.UserDetailView.as_view(),
        name='user_detail'
    ),
    url(
        r'users/(?P<pk>\d+)/does-not-have-permissions/',
        views.UserDoesNotHavePermissionsView.as_view(),
        name='user_does_not_have_permissions'
    ),

    # Roles views
    url(
        r'^roles/$',
        views.RoleListView.as_view(),
        name='role_list'
    ),
    url(
        r'^roles/add/$',
        views.RoleCreateView.as_view(),
        name='role_create'
    ),
    url(
        r'^role/(?P<pk>\d+)/update/$',
        views.RoleUpdateView.as_view(),
        name='role_update'
    ),
    url(
        r'^role/(?P<pk>\d+)/delete/$',
        views.RoleDeleteView.as_view(),
        name='role_delete'
    ),

    # Profiles views
    url(
        r'^users/(?P<pk>\d+)/profiles/add/$',
        views.ProfileCreateView.as_view(),
        name='profile_create'
    ),
    url(
        r'^users/profiles/(?P<pk>\d+)/update/$',
        views.ProfileUpdateView.as_view(),
        name='profile_update'
    ),
    url(
        r'^users/profiles/(?P<pk>\d+)/delete/$',
        views.ProfileDeleteView.as_view(),
        name='profile_delete'
    ),
    url(
        r'^users/profiles/(?P<pk>\d+)/detail/$',
        views.ProfileDetailView.as_view(),
        name='profile_detail'
    ),
    url(
        r'^users/(?P<user_pk>\d+)/profiles/(?P<pk>\d+)/update/$',
        views.UsersProfileUpdateView.as_view(),
        name='users_profile_update'
    ),

    # Groups views
    url(
        r'^groups/$',
        views.GroupListView.as_view(),
        name='group_list'
    ),
    url(
        r'^groups/add/$',
        views.GroupCreateView.as_view(),
        name='group_create'
    ),
    url(
        r'^groups/(?P<pk>\d+)/update/$',
        views.GroupUpdateView.as_view(),
        name='group_update'
    ),
    url(
        r'^groups/(?P<pk>\d+)/delete/$',
        views.GroupDeleteView.as_view(),
        name='group_delete'
    ),
]
