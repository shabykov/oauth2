from django.conf.urls import url

from . import views

urlpatterns = [

    # Users views
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
    ),
    url(
        r'^core/users/(?P<pk>\d+)/delete/$',
        views.UserDeleteView.as_view(),
        name='user_delete'
    ),

    # Roles views
    url(
        r'^core/roles/$',
        views.RoleListView.as_view(),
        name='role_list'
    ),
    url(
        r'^core/roles/add/$',
        views.RoleCreateView.as_view(),
        name='role_create'
    ),
    url(
        r'^core/role/(?P<pk>\d+)/update/$',
        views.RoleUpdateView.as_view(),
        name='role_update'
    ),
    url(
        r'^core/role/(?P<pk>\d+)/delete/$',
        views.RoleDeleteView.as_view(),
        name='role_delete'
    ),

    # Profiles views
    url(
        r'^core/users/(?P<pk>\d+)/profiles/add/$',
        views.ProfileCreateView.as_view(),
        name='profile_create'
    ),
    url(
        r'^core/users/profiles/(?P<pk>\d+)/update/$',
        views.ProfileUpdateView.as_view(),
        name='profile_update'
    ),
    url(
        r'^core/users/profiles/(?P<pk>\d+)/delete/$',
        views.ProfileDeleteView.as_view(),
        name='profile_delete'
    ),
    url(
        r'^core/users/(?P<user_pk>\d+)/profiles/(?P<pk>\d+)/update/$',
        views.UsersProfileUpdateView.as_view(),
        name='users_profile_update'
    ),

    # Groups views
    url(
        r'^core/groups/$',
        views.GroupListView.as_view(),
        name='group_list'
    ),
    url(
        r'^core/groups/add/$',
        views.GroupCreateView.as_view(),
        name='group_create'
    ),
    url(
        r'^core/groups/(?P<pk>\d+)/update/$',
        views.GroupUpdateView.as_view(),
        name='group_update'
    ),
    url(
        r'^core/groups/(?P<pk>\d+)/delete/$',
        views.GroupDeleteView.as_view(),
        name='group_delete'
    ),
]
