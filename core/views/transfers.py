from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from core.serializers import (
    AccountToDepositTransferSerializer, AccountToLoanTransferSerializer,
    DepositToAccountTransferSerializer
)

# TODO:
#  DepositToCreditTransfer
#  AccountToAccountTransfer (by iban, phone number)
#  CardToAccount (card num -> account iban)


class TransferViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['POST'], url_path='account_to_loan')
    def from_account_to_loan(self, request):
        serializer = AccountToLoanTransferSerializer(data=request.data,
                                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='account_to_deposit')
    def from_account_to_deposit(self, request):
        serializer = AccountToDepositTransferSerializer(data=request.data,
                                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='deposit_to_account')
    def from_deposit_to_account(self, request):
        serializer = DepositToAccountTransferSerializer(data=request.data,
                                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

