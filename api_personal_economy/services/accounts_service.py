from django.db.models import Sum

from api_personal_economy.models import Account
from api_personal_economy.serializers.accounts import AccountSerializer


def create(serializer: AccountSerializer, current_user):
    initial_balance = serializer.validated_data['initial_balance']
    return serializer.save(owner=current_user, balance=initial_balance)


def update(serializer: AccountSerializer):
    instance = serializer.instance
    validated_data = serializer.validated_data
    balance = instance.balance

    if validated_data['initial_balance'] != instance.initial_balance:
        difference = validated_data['initial_balance'] - instance.initial_balance
        balance += difference

    return serializer.save(balance=balance)


def destroy(account: Account):
    account.active = False
    account.name += '-deleted'
    account.save()


def get_total_balance(user):
    total = (Account.objects
             .filter(owner=user, active=True)
             .aggregate(total=Sum('balance'))['total'])

    return total
