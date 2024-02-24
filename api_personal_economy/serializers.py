import string

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_personal_economy.models import Cuenta, Operacion


# Serializers define the API representation.
class CuentaSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    operaciones = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cuenta
        fields = ['id', 'url', 'nombre', 'owner', 'balance', 'operaciones']
        read_only_fields = ['balance', ]
        validators = [
            UniqueTogetherValidator(
                queryset=Cuenta.objects.filter(active=True),
                fields=['nombre', 'owner'],
                message='Este usuario ya posee una cuenta con este nombre'
            )
        ]

    def validate_nombre(self, value: str):
        if value[0].isdigit():
            raise serializers.ValidationError(
                "El nombre de la cuenta no puede comenzar con un número.")
        return value.capitalize()


class OperacionSerializer(serializers.HyperlinkedModelSerializer):
    # cuenta = serializers.rela()

    class Meta:
        model = Operacion
        fields = ['id', 'url', 'tipo', 'cuenta', 'fecha', 'monto', 'descripcion']
        # depth = 1

    def validate(self, data):
        """
        Comprobar que el monto del gasto no sea mayor que el balance de la cuenta.
        Si se está editando la operación comprobar que el cambio en el gasto no sobrepase el balance de la cuenta.
        """
        if data['tipo'] == 'Ga':
            cuenta = data['cuenta']
            monto = data['monto']
            instance = self.instance
            if instance is None or (instance and instance.cuenta != cuenta):
                if cuenta.balance < monto:
                    raise serializers.ValidationError(
                        "La cuenta indicada no posee balance suficiente para realizar este gasto.")
            elif instance.tipo == 'Ga':  # Solo viene aqui si es una edicion y la cuenta no cambia
                if monto > instance.monto:  # Si el nuevo monto es mayor que el anterior compruebo el balance.
                    diferencia = monto - instance.monto
                    if cuenta.balance < diferencia:
                        raise serializers.ValidationError(
                            "La cuenta indicada no posee balance suficiente para realizar este gasto.")
            else:
                if cuenta.balance < instance.monto + monto:
                    raise serializers.ValidationError(
                        "La cuenta indicada no posee balance suficiente para realizar este gasto.")
        return data

    def validate_cuenta(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("Usted no es propietario de la cuenta indicada.")
        return value

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser un valor positivo.")
        return value
