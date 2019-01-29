from oauth2_provider import views
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import permissions, generics
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from ...serializers import UserSerializer


class ApiEndpoint(views.generic.ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


class GetUserView(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.pk)
