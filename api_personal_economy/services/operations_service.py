from api_personal_economy.models import Operation, Account
from api_personal_economy.serializers.operations import OperationSerializer, OperationInputSerializer


def create(serializer: OperationInputSerializer):
    instance = serializer.save()
    update_balance(instance.account, instance.type, instance.amount)
    return instance


def update(serializer: OperationInputSerializer):
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


def destroy_bulk(ids: list):
    operations_to_delete = Operation.objects.filter(pk__in=ids).select_related('account')
    operations_to_delete.update(active=False)
    operations_grouped = {}

    for operation in operations_to_delete:
        account_id = operation.account.id
        if account_id not in operations_grouped:
            operations_grouped[account_id] = {
                "account": operation.account,
                "amount": 0
            }
        operations_grouped[account_id]["amount"] += operation.amount if operation.type == Operation.Expense \
            else -1 * operation.amount

    for operation in operations_grouped.values():
        update_balance(operation["account"], Operation.INCOME, operation["amount"])


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
