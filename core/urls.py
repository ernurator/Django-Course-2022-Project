from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import (
    BankAccountListCreateAPIView, BankAccountRetrieveDestroyAPIView,
    DebitCardViewSet,
    DepositViewSet, charge_interest_on_deposit_api_view,
    LoanViewSet, charge_interest_on_loan_api_view,
    TransferViewSet
)

urlpatterns = [
    path('accounts/', BankAccountListCreateAPIView.as_view()),
    path('accounts/<str:iban>/', BankAccountRetrieveDestroyAPIView.as_view()),
    path('charge_interests/deposits/<str:iban>/', charge_interest_on_deposit_api_view),
    path('charge_interests/loans/<int:id_>/', charge_interest_on_loan_api_view)
]

router = SimpleRouter()
router.register(r'cards', DebitCardViewSet, basename='debit-card')
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'transfers', TransferViewSet, basename='transfer')
urlpatterns.extend(router.urls)
