from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserAPIView, UserDocumentsAPIView

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('users/', UserAPIView.as_view()),
]

router = SimpleRouter()
router.register(r'documents', UserDocumentsAPIView, basename='document')
urlpatterns.extend(router.urls)
