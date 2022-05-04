from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import DebitCard
from core.serializers import DebitCardReadSerializer, DebitCardUpdateSerializer, DebitCardCreateSerializer


class DebitCardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def get_queryset(self):
        user = self.request.user
        return DebitCard.objects.user_cards(user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET', 'DELETE'):
            return DebitCardReadSerializer
        elif method in ('PUT', 'PATCH'):
            return DebitCardUpdateSerializer
        else:
            return DebitCardCreateSerializer
