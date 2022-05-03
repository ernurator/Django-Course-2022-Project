from .account import BankAccountReadSerializer, BankAccountWriteSerializer  # noqa
from .card import DebitCardWriteSerializer, DebitCardUpdateSerializer, DebitCardReadSerializer  # noqa
from .deposit import DepositReadSerializer, DepositWriteSerializer  # noqa
from .loan import LoanReadSerializer, LoanWriteSerializer, LoanUpdateSerializer  # noqa

from .transfers import AccountToDepositTransferSerializer  # noqa
