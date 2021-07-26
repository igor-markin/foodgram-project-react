from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from api.models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'password',
                  'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()
