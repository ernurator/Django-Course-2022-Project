from .account import BankAccountReadSerializer, BankAccountCreateSerializer  # noqa
from .card import DebitCardCreateSerializer, DebitCardUpdateSerializer, DebitCardReadSerializer  # noqa
from .deposit import DepositReadSerializer, DepositCreateSerializer  # noqa
from .loan import LoanReadSerializer, LoanCreateSerializer  # noqa

from .transfers import (
    AccountToDepositTransferSerializer, AccountToLoanTransferSerializer,
    DepositToAccountTransferSerializer, DepositToLoanTransferSerializer,
    AccountToAccountTransferSerializer, CardToAccountTransferSerializer
)
