from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_personal_economy.models import Account, Operation


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    accounts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'is_staff', 'accounts']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data: dict):
        passw = validated_data.pop('password')
        user: User = super().update(instance, validated_data)
        user.set_password(passw)
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
