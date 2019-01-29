from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^accounts/login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),

    # url(r'^accounts/reset-password', PasswordResetView.as_view(), name='reset-password'),
    # url(r'^accounts/change-password/$', PasswordChangeView.as_view(), name='change-password'),
    # url(r'^accounts/change-password/$', PasswordChangeView.as_view(), name='change-password'),
]
