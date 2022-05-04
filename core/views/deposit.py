from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated

from core.models import Deposit
from core.serializers import DepositReadSerializer, DepositCreateSerializer
from core.permissions import IsSuperuser
from core.throttles import OncePerDayUserThrottle


@api_view(['POST'])
@throttle_classes([OncePerDayUserThrottle])
@permission_classes([IsSuperuser])
def charge_interest_on_deposit_api_view(request, iban=None):
    deposit = Deposit.objects.get_user_deposit(request.user, iban=iban)
    if not deposit:
        return Response({'message': f'Deposit #{iban} not found'}, status=HTTP_400_BAD_REQUEST)
    deposit.balance = (1 + deposit.rate / 100 / 365) * deposit.balance
    deposit.save()
    return Response({'message': f'Balance of deposit #{iban} updated!'})


class DepositViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Deposit.objects.user_deposits(user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET',):
            return DepositReadSerializer
        if method in ('POST',):
            return DepositCreateSerializer
        raise ValueError(f'Unhandled method {method}')
