from rest_framework import serializers

from api_personal_economy.models import Operation
from api_personal_economy.serializers.accounts import AccountMinimalOutputSerializer


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountMinimalOutputSerializer()

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


class OperationMinimalOutputSerializer(serializers.ModelSerializer):
    account = AccountMinimalOutputSerializer()

    class Meta:
        model = Operation
        fields = ['id', 'type', 'account', 'date', 'amount', 'description']
