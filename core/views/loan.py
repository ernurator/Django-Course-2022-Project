from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Loan
from core.serializers import LoanReadSerializer, LoanUpdateSerializer, LoanWriteSerializer


class LoanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.user_loans(user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET', 'DELETE'):
            return LoanReadSerializer
        elif method in ('PUT', 'PATCH'):
            return LoanUpdateSerializer
        else:
            return LoanWriteSerializer
