from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api_personal_economy.serializers.accounts import AccountSerializer
from api_personal_economy.models import Account
from api_personal_economy.services import accounts_service


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
        accounts_service.create(serializer, self.request.user)

    def perform_update(self, serializer):
        accounts_service.update(serializer)

    def perform_destroy(self, instance: Account):
        accounts_service.destroy(instance)

    @action(methods=['get'], url_path='get-total-balance', detail=False)
    def get_total_balance(self, request):
        total = accounts_service.get_total_balance(request.user)
        return Response({'total': total})
