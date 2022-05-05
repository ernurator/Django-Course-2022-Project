from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import UserAPIView, UserDocumentsAPIView

urlpatterns = [
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('users/', UserAPIView.as_view()),
]

router = SimpleRouter()
router.register(r'documents', UserDocumentsAPIView, basename='document')
urlpatterns.extend(router.urls)
