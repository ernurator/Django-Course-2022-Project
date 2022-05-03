from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers import AccountToDepositTransferSerializer

# TODO:
#  AccountToCreditTransfer
#  DepositToAccountTransfer
#  DepositToCreditTransfer
#  AccountToAccountTransfer (by iban, phone number)
#  CardToAccount (card num -> account iban)


@api_view(['POST'])
def transfer_from_account_to_deposit(request):
    serializer = AccountToDepositTransferSerializer(data=request.data,
                                                    context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
