from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^core/users/$',
        views.UserListView.as_view(),
        name='user_list'
    ),
    url(
        r'^core/users/add/$',
        views.UserCreateView.as_view(),
        name='user_create'
    ),
    url(
        r'^core/users/(?P<pk>\d+)/update/$',
        views.UserUpdateView.as_view(),
        name='user_update'
    )
]
