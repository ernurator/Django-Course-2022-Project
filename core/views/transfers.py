from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from core.serializers import AccountToDepositTransferSerializer, AccountToLoanTransferSerializer

# TODO:
#  DepositToAccountTransfer
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


@api_view(['POST'])
def transfer_from_account_to_deposit(request):
    serializer = AccountToDepositTransferSerializer(data=request.data,
                                                    context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
