from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from oauth2_provider.models import get_access_token_model, get_application_model


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'phone', 'first_name', 'last_name', 'patronymic',
            'is_active', 'is_staff', 'date_joined', 'groups', 'user_permissions')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_application_model()
        fields = ('client_id', 'name', 'client_type', 'redirect_uris', 'created', 'updated')


class AccessTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    application = ApplicationSerializer()
    expired = serializers.SerializerMethodField(method_name='is_token_expired')

    class Meta:
        model = get_access_token_model()
        fields = ('user', 'token', 'application', 'expires', 'scope', 'expired')

    def is_token_expired(self, obj):
        return obj.is_expired()
