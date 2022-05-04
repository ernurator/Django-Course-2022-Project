from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .models import User, UserDocuments
from .serializers import (
    UserSerializer, UserCreateSerializer,
    UserDocumentsReadSerializer, UserDocumentsCreateSerializer
)


class UserAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('date_joined')

    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST':
            return UserCreateSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        method = self.request.method
        if method == 'POST':
            return [AllowAny()]
        else:
            return [IsAdminUser()]


class UserDocumentsAPIView(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]  # TODO: remove after enabling IsAuthenticated in global settings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return UserDocuments.objects.filter(user=user)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('GET',):
            return UserDocumentsReadSerializer
        if method in ('POST',):
            return UserDocumentsCreateSerializer
        raise ValueError(f'Unhandled method {method}')
