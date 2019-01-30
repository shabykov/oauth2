from oauth2_provider import views
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes


from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from ...serializers import UserSerializer


class ApiEndpoint(views.generic.ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([OAuth2Authentication])
def get_user_view(request):
    if not request.user.is_anonymous:
        return Response(data=UserSerializer(request.user).data, status=200)
    return Response(data={'error': 'user is anonymous'}, status=404)

