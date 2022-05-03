from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import User
from .serializers import UserSerializer, UserCreateSerializer


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
