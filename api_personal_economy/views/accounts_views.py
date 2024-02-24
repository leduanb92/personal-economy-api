from rest_framework import viewsets
from rest_framework import permissions

from api_personal_economy.serializers.accounts import AccountSerializer
from api_personal_economy.models import Account


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
