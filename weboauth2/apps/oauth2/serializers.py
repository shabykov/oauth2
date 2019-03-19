from rest_framework import serializers
from django.contrib.auth import get_user_model
from oauth2_provider.models import get_access_token_model, get_application_model

from ..accounts.models import Profile, Role


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_application_model()
        fields = ('client_id', 'name', 'client_type', 'redirect_uris', 'created', 'updated')


class RoleSerializer(serializers.ModelSerializer):

    id_display = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ('scope', 'id_display',)

    def get_id_display(self, obj):
        return obj.get_id_display()


class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    applications = ApplicationSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('role', 'applications',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'phone', 'first_name', 'last_name', 'patronymic',
            'is_active', 'is_staff', 'date_joined', 'profile',)


class AccessTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    application = ApplicationSerializer()
    expired = serializers.SerializerMethodField(method_name='is_token_expired')

    class Meta:
        model = get_access_token_model()
        fields = ('user', 'token', 'application', 'expires', 'scope', 'expired')

    def is_token_expired(self, obj):
        return obj.is_expired()
