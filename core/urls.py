from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import (
    BankAccountListCreateAPIView, BankAccountRetrieveDestroyAPIView,
    DebitCardViewSet,
    DepositViewSet,
    LoanViewSet,
    transfer_from_account_to_deposit,
    TransferViewSet
)

urlpatterns = [
    path('accounts/', BankAccountListCreateAPIView.as_view()),
    path('accounts/<str:iban>/', BankAccountRetrieveDestroyAPIView.as_view()),
    path('transfers/account_to_deposit/', transfer_from_account_to_deposit)
]

router = SimpleRouter()
router.register(r'cards', DebitCardViewSet, basename='debit-card')
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'transfers', TransferViewSet, basename='transfer')
urlpatterns.extend(router.urls)
