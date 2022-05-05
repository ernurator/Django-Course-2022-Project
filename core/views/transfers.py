from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.serializers import (
    AccountToDepositTransferSerializer, AccountToLoanTransferSerializer,
    DepositToAccountTransferSerializer, DepositToLoanTransferSerializer,
    AccountToAccountTransferSerializer, CardToAccountTransferSerializer
)


class TransferViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

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

    @action(detail=False, methods=['POST'], url_path='deposit_to_loan')
    def from_deposit_to_loan(self, request):
        serializer = DepositToLoanTransferSerializer(data=request.data,
                                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='account_to_account')
    def from_account_to_account(self, request):
        serializer = AccountToAccountTransferSerializer(data=request.data,
                                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='card_to_account')
    def from_card_to_account(self, request):
        serializer = CardToAccountTransferSerializer(data=request.data,
                                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
