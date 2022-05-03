from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.models import Deposit
from core.serializers import DepositReadSerializer, DepositWriteSerializer

# TODO: Add interest on deposit view


class DepositViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Deposit.objects.user_deposits(user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET', 'DELETE'):
            return DepositReadSerializer
        if method in ('POST',):
            return DepositWriteSerializer
        raise ValueError(f'Unhandled method {method}')
