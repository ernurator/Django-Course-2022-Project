from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import (
    BankAccountListCreateAPIView, BankAccountRetrieveDestroyAPIView,
    DebitCardViewSet,
    DepositViewSet,
    LoanViewSet
)

urlpatterns = [
    path('accounts/', BankAccountListCreateAPIView.as_view()),
    path('accounts/<str:iban>/', BankAccountRetrieveDestroyAPIView.as_view()),
]

router = SimpleRouter()
router.register(r'cards', DebitCardViewSet, basename='debit-card')
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'loans', LoanViewSet, basename='loan')
urlpatterns.extend(router.urls)