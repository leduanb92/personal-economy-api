from api_personal_economy.models import Operation, Account
from api_personal_economy.serializers.operations import OperationSerializer


def create(serializer: OperationSerializer):
    instance = serializer.save()
    update_balance(instance.account, instance.type, instance.amount)
    return instance


def update(serializer):
    old_value = serializer.instance
    new_value = serializer.validated_data
    if old_value.account == new_value['account']:
        if old_value.type == new_value['type'] and old_value.amount != new_value['amount']:
            difference = new_value['amount'] - old_value.amount
            update_balance(old_value.account, new_value['type'], difference)
        elif old_value.type != new_value['type']:
            update_balance(old_value.account, new_value['type'], old_value.amount)
            update_balance(old_value.account, new_value['type'], new_value['amount'])
    else:
        update_balance(old_value.account, old_value.type, -1 * old_value.amount)
        update_balance(new_value['account'], new_value['type'], new_value['amount'])

    return serializer.save()


def destroy(operation: Operation):
    operation.active = False
    operation.save()
    update_balance(operation.account, operation.type, -1 * operation.amount)


def update_balance(account: Account, op_type, amount):
    if op_type == Operation.INCOME:
        account.balance += amount
    else:
        account.balance -= amount
    account.save()


def get_operations_by_date(request, date, serializer_class=OperationSerializer):
    operations = Operation.objects.filter(account__owner=request.user, date=date, active=True).order_by('updated_at')
    if operations:
        return serializer_class(operations, many=True, context={'request': request}).data
    return []