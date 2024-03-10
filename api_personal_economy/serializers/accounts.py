from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_personal_economy.models import Account


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    operations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'url', 'name', 'owner', 'initial_balance', 'balance', 'operations']
        read_only_fields = ['balance', ]
        validators = [
            UniqueTogetherValidator(
                queryset=Account.objects.filter(active=True),
                fields=['name', 'owner'],
                message='This user already has an account with this name.'
            )
        ]

    def validate_name(self, value: str):
        if value[0].isdigit():
            raise serializers.ValidationError("The name of the account can not start with a number.")
        return value


class AccountMinimalOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance']
        read_only_fields = ['id', 'name', 'balance']
