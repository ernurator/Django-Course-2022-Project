import logging

from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated

from core.models import Loan
from core.serializers import LoanReadSerializer, LoanCreateSerializer
from core.permissions import IsSuperuser
from core.throttles import OncePerDayUserThrottle

logger = logging.getLogger(__name__)


@api_view(['POST'])
@throttle_classes([OncePerDayUserThrottle])
@permission_classes([IsSuperuser])
def charge_interest_on_loan_api_view(request, id_=None):
    loan = Loan.objects.get_user_loan(request.user, id_=id_)
    if not loan:
        return Response({'message': f'Loan #{id_} not found'}, status=HTTP_400_BAD_REQUEST)
    logger.debug(f'Charging interest on loan {loan}')
    loan.balance = (1 + loan.rate / 100 / 365) * loan.balance
    loan.save()
    return Response({'message': f'Balance of loan #{id_} updated!'})


class LoanViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.user_loans(user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET',):
            return LoanReadSerializer
        if method in ('POST',):
            return LoanCreateSerializer
        raise ValueError(f'Unhandled method {method}')
