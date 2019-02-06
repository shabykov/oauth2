import logging

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from oauth2_provider.models import get_access_token_model
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from ...serializers import UserSerializer, AccessTokenSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([OAuth2Authentication])
def get_user_view(request):
    if not request.user.is_anonymous:
        return Response(data=UserSerializer(request.user).data, status=200, content_type="application/json; charset=utf-8")
    return Response(data={'error': 'user {} is anonymous'.format(request.user)}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([OAuth2Authentication])
def get_access_token(request):
    model = get_access_token_model()
    if not request.user.is_anonymous:
        try:
            return Response(data=AccessTokenSerializer(model.objects.get(token=request.auth)).data, status=200, content_type="application/json; charset=utf-8")
        except model.DoesNotExist as error:
            logging.error(error)
            return Response(data={'error': 'user {} does not have access_token'.format(request.user)})
    return Response(data={'error': 'user {} is anonymous'.format(request.user)})
