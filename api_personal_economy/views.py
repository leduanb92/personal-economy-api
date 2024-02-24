from copy import deepcopy, copy

from rest_framework import viewsets, status
from rest_framework import permissions

from api_personal_economy.serializers import CuentaSerializer, OperacionSerializer
from api_personal_economy.models import Cuenta, Operacion
# from api_personal_economy.permissions import IsOwner, IsOwnerOfCuenta


class CuentaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Cuentas to be viewed or edited.
    """
    queryset = Cuenta.objects.none()
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cuenta.objects.filter(owner=user, active=True)

    def perform_create(self, serializer):
        if serializer.is_valid():
            # serializer.save(owner=self.request.user)
            instance = serializer.save(owner=self.request.user)
            instance.nombre = instance.nombre.capitalize()
            instance.save()

    def perform_destroy(self, instance: Cuenta):
        instance.active = False
        instance.nombre += '-deleted'
        instance.save()


class OperacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Operaciones to be viewed or edited.
    """
    queryset = Operacion.objects.none()
    serializer_class = OperacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        self.queryset = Operacion.objects.filter(cuenta__owner=user, active=True)
        cuenta_id = self.request.query_params.get('cuenta_id', None)
        if cuenta_id:
            self.queryset = self.queryset.filter(cuenta__id=cuenta_id)
        return self.queryset

    def perform_create(self, serializer: OperacionSerializer):
        if serializer.is_valid():
            instance = serializer.save()
            self.update_balance(instance.cuenta, instance.tipo, instance.monto)

    def perform_update(self, serializer: OperacionSerializer):
        old_value = serializer.instance
        new_value = serializer.validated_data
        if old_value.cuenta == new_value['cuenta']:
            if old_value.tipo == new_value['tipo'] and old_value.monto != new_value['monto']:
                diferencia = new_value['monto'] - old_value.monto
                self.update_balance(old_value.cuenta, new_value['tipo'], diferencia)
            elif old_value.tipo != new_value['tipo']:
                self.update_balance(old_value.cuenta, new_value['tipo'], old_value.monto)
                self.update_balance(old_value.cuenta, new_value['tipo'], new_value['monto'])
        else:
            self.update_balance(old_value.cuenta, old_value.tipo, -1 * old_value.monto)
            self.update_balance(new_value['cuenta'], new_value['tipo'], new_value['monto'])

        print(old_value.cuenta, '\n', new_value['cuenta'])
        serializer.save()

    def update_balance(self, cuenta: Cuenta, tipo_op, monto):
        if tipo_op == 'In':
            cuenta.balance += monto
        else:
            cuenta.balance -= monto
        cuenta.save()
