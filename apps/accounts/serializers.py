from rest_framework import serializers
from accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile_pic_url',
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
        ]