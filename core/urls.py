from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import BankAccountListCreateAPIView, BankAccountRetrieveUpdateDestroyAPIView, DebitCardViewSet

urlpatterns = [
    path('accounts/', BankAccountListCreateAPIView.as_view()),
    path('accounts/<str:iban>/', BankAccountRetrieveUpdateDestroyAPIView.as_view()),
]

router = SimpleRouter()
router.register(r'cards', DebitCardViewSet, basename='debit-card')
urlpatterns.extend(router.urls)

