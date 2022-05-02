from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import (
    BankAccountListCreateAPIView, BankAccountRetrieveDestroyAPIView,
    DebitCardViewSet,
    DepositViewSet, transfer_from_account_to_deposit,
    LoanViewSet
)

urlpatterns = [
    path('accounts/', BankAccountListCreateAPIView.as_view()),
    path('accounts/<str:iban>/', BankAccountRetrieveDestroyAPIView.as_view()),
    path('deposits/<str:deposit_pk>/transfer_from_account/', transfer_from_account_to_deposit)
]

router = SimpleRouter()
router.register(r'cards', DebitCardViewSet, basename='debit-card')
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'loans', LoanViewSet, basename='loan')
urlpatterns.extend(router.urls)
