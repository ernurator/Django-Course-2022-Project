from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.models import Loan
from core.serializers import LoanReadSerializer, LoanCreateSerializer

# TODO: Create view charging interests on loan


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
