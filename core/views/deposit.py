from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Deposit
from core.serializers import DepositReadSerializer, DepositUpdateSerializer, DepositWriteSerializer


class DepositViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Deposit.objects.filter(user=user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET', 'DELETE'):
            return DepositReadSerializer
        elif method in ('PUT', 'PATCH'):
            return DepositUpdateSerializer
        else:
            return DepositWriteSerializer
