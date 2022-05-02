from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from .views import UserAPIView

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('users/', UserAPIView.as_view()),
]
