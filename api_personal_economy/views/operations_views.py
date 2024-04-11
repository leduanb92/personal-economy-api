from datetime import datetime

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api_personal_economy.serializers.operations import OperationInputSerializer, OperationMinimalOutputSerializer
from api_personal_economy.models import Operation
from api_personal_economy.services import operations_service


class OperationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Operations to be viewed or edited.
    """
    queryset = Operation.objects.none()
    serializer_class = OperationMinimalOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        self.queryset = Operation.objects.filter(account__owner=user, active=True)
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            self.queryset = self.queryset.filter(account__id=account_id)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OperationInputSerializer
        return self.serializer_class

    def perform_create(self, serializer: OperationInputSerializer):
        operations_service.create(serializer)

    def perform_update(self, serializer: OperationInputSerializer):
        operations_service.update(serializer)

    def perform_destroy(self, instance: Operation):
        operations_service.destroy(instance)

    @action(methods=['get'], url_path='by-date', detail=False)
    def by_date(self, request):
        date = request.query_params.get('date', None)
        if not date:
            return Response({'error': 'You must specify a date'}, status=400)
        date = datetime.strptime(date, '%Y-%m-%d')
        operations = operations_service.get_operations_by_date(request, date)
        return Response({'list': operations})
