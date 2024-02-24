from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_personal_economy.models import Account, Operation


# Serializers define the API representation.
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
            raise serializers.ValidationError(
                "The name of the account can not start with a number.")
        return value.capitalize()


class OperationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Operation
        fields = ['id', 'url', 'type', 'account', 'date', 'amount', 'description']

    def validate(self, data):
        """
        Comprobar que el amount del gasto no sea mayor que el balance de la account.
        Si se está editando la operación comprobar que el cambio en el gasto no sobrepase el balance de la account.
        """
        if data['type'] == Operation.Expense:
            account = data['account']
            amount = data['amount']
            instance = self.instance
            if instance is None or (instance and instance.account != account):
                if account.balance < amount:
                    raise serializers.ValidationError(
                        "The specified account does not have enough balance to perform this expense.")
            elif instance.type == Operation.Expense:  # Solo viene aqui si es una edicion y la account no cambia
                if amount > instance.amount:  # Si el nuevo amount es mayor que el anterior compruebo el balance.
                    difference = amount - instance.amount
                    if account.balance < difference:
                        raise serializers.ValidationError(
                            "The specified account does not have enough balance to perform this expense.")
            else:
                if account.balance < instance.amount + amount:
                    raise serializers.ValidationError(
                        "The specified account does not have enough balance to perform this expense.")
        return data

    def validate_account(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("You are not the owner of this account.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The amount must be greater than 0.")
        return value
