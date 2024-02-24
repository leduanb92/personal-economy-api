from rest_framework import viewsets, status
from rest_framework import permissions

from api_personal_economy.serializers import AccountSerializer, OperationSerializer
from api_personal_economy.models import Account, Operation


class AccountsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Accounts to be viewed or edited.
    """
    queryset = Account.objects.none()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(owner=user, active=True)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        instance.name = instance.name.capitalize()
        instance.save()

    def perform_destroy(self, instance: Account):
        instance.active = False
        instance.name += '-deleted'
        instance.save()


class OperationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Operations to be viewed or edited.
    """
    queryset = Operation.objects.none()
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        self.queryset = Operation.objects.filter(account__owner=user, active=True)
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            self.queryset = self.queryset.filter(account__id=account_id)
        return self.queryset

    def perform_create(self, serializer: OperationSerializer):
        instance = serializer.save()
        self.update_balance(instance.account, instance.type, instance.amount)

    def perform_update(self, serializer: OperationSerializer):
        old_value = serializer.instance
        new_value = serializer.validated_data
        if old_value.account == new_value['account']:
            if old_value.type == new_value['type'] and old_value.amount != new_value['amount']:
                difference = new_value['amount'] - old_value.amount
                self.update_balance(old_value.account, new_value['type'], difference)
            elif old_value.type != new_value['type']:
                self.update_balance(old_value.account, new_value['type'], old_value.amount)
                self.update_balance(old_value.account, new_value['type'], new_value['amount'])
        else:
            self.update_balance(old_value.account, old_value.type, -1 * old_value.amount)
            self.update_balance(new_value['account'], new_value['type'], new_value['amount'])

        print(old_value.account, '\n', new_value['account'])
        serializer.save()

    def update_balance(self, account: Account, op_type, amount):
        if op_type == Operation.INCOME:
            account.balance += amount
        else:
            account.balance -= amount
        account.save()
