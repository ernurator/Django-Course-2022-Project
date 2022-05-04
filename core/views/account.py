from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.serializers import BankAccountReadSerializer, BankAccountCreateSerializer
from core.models import BankAccount


class BankAccountBaseAPIView(generics.GenericAPIView):
    lookup_field = 'iban'
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def get_queryset(self):
        return BankAccount.objects.user_accounts(self.request.user)


class BankAccountListCreateAPIView(BankAccountBaseAPIView, generics.ListCreateAPIView):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return BankAccountReadSerializer
        else:
            return BankAccountCreateSerializer


class BankAccountRetrieveDestroyAPIView(BankAccountBaseAPIView, generics.RetrieveDestroyAPIView):
    serializer_class = BankAccountReadSerializer
