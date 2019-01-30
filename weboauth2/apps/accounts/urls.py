from django.conf.urls import url

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
        views.views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    url(
        r'^accounts/logout/$',
        views.LogoutView.as_view(),
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
]
