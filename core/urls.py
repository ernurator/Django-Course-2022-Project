from django.urls import path

from .views import BankAccountListCreateAPIView, BankAccountRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('accounts/', BankAccountListCreateAPIView.as_view()),
    path('accounts/<str:iban>/', BankAccountRetrieveUpdateDestroyAPIView.as_view()),
]
