import logging

from django.db import transaction
from django.core.validators import MinValueValidator

from rest_framework import serializers

from core.models import BankAccount, Deposit, Loan, DebitCard

logger = logging.getLogger(__name__)


class TransferBaseSerializer(serializers.Serializer):
    def _get_user_from_context(self):
        return self.context['request'].user

    def _get_account(self, iban):
        return BankAccount.objects.get_user_account(user=self._get_user_from_context(), iban=iban)

    def _get_deposit(self, iban):
        return Deposit.objects.get_user_deposit(user=self._get_user_from_context(), iban=iban)

    def _get_loan(self, id_):
        return Loan.objects.get_user_loan(user=self._get_user_from_context(), id_=id_)

    def validate_deposit_iban(self, value):
        if not self._get_deposit(value):
            raise serializers.ValidationError(f'Wrong deposit provided: #{value}')
        return value

    def validate_account_iban(self, value):
        if not self._get_account(value):
            raise serializers.ValidationError(f'Wrong account provided: #{value}')
        return value

    def validate_loan_id(self, value):
        if not self._get_loan(value):
            raise serializers.ValidationError(f'Wrong loan id provided: #{value}')
        return value

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def save(self, **kwargs):
        raise NotImplementedError


class AccountToDepositTransferSerializer(TransferBaseSerializer):
    deposit_iban = serializers.UUIDField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate(self, attrs):
        amount = attrs['amount']
        account = self._get_account(attrs['account_iban'])
        deposit = self._get_deposit(attrs['deposit_iban'])
        if account.currency != deposit.currency:
            raise serializers.ValidationError('Currencies of the account and the deposit do not match')
        if account.balance < amount:
            raise serializers.ValidationError('Not enough balance on the account')
        return attrs

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        account = self._get_account(self.validated_data['account_iban'])
        deposit = self._get_deposit(self.validated_data['deposit_iban'])
        with transaction.atomic():
            try:
                logger.debug(f'Starting transfer from {account} to {deposit}')
                account.balance -= amount
                deposit.balance += amount
                account.save()
                deposit.save()
            except Exception as e:
                logger.error(f'Transfer from {account} to {deposit} failed with following exception: {e}')
                raise


class AccountToLoanTransferSerializer(TransferBaseSerializer):
    loan_id = serializers.IntegerField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate(self, attrs):
        amount = attrs['amount']
        account = self._get_account(attrs['account_iban'])
        loan = self._get_loan(attrs['loan_id'])
        if account.currency != loan.currency:
            raise serializers.ValidationError('Currencies of the account and the loan do not match')
        if account.balance < amount:
            raise serializers.ValidationError('Not enough balance on the account')
        if loan.balance < amount:
            raise serializers.ValidationError('Too high transfer amount, loan will be over-payed')
        return attrs

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        account = self._get_account(self.validated_data['account_iban'])
        loan = self._get_loan(self.validated_data['loan_id'])
        with transaction.atomic():
            try:
                logger.debug(f'Starting transfer from {account} to {loan}')
                account.balance -= amount
                loan.balance -= amount
                account.save()
                loan.save()
            except Exception as e:
                logger.error(f'Transfer from {account} to {loan} failed with following exception: {e}')
                raise


class DepositToAccountTransferSerializer(TransferBaseSerializer):
    deposit_iban = serializers.UUIDField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate(self, attrs):
        amount = attrs['amount']
        account = self._get_account(attrs['account_iban'])
        deposit = self._get_deposit(attrs['deposit_iban'])
        if account.currency != deposit.currency:
            raise serializers.ValidationError('Currencies of the account and the deposit do not match')
        if deposit.balance < amount:
            raise serializers.ValidationError('Not enough balance on the deposit')
        return attrs

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        account = self._get_account(self.validated_data['account_iban'])
        deposit = self._get_deposit(self.validated_data['deposit_iban'])
        with transaction.atomic():
            try:
                logger.debug(f'Starting transfer from {deposit} to {account}')
                account.balance += amount
                deposit.balance -= amount
                account.save()
                deposit.save()
            except Exception as e:
                logger.error(f'Transfer from {deposit} to {account} failed with following exception: {e}')
                raise


class DepositToLoanTransferSerializer(TransferBaseSerializer):
    loan_id = serializers.IntegerField()
    deposit_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate(self, attrs):
        amount = attrs['amount']
        deposit = self._get_deposit(attrs['deposit_iban'])
        loan = self._get_loan(attrs['loan_id'])
        if deposit.currency != loan.currency:
            raise serializers.ValidationError('Currencies of the deposit and the loan do not match')
        if deposit.balance < amount:
            raise serializers.ValidationError('Not enough balance on the deposit')
        if loan.balance < amount:
            raise serializers.ValidationError('Too high transfer amount, loan will be over-payed')
        return attrs

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        deposit = self._get_deposit(self.validated_data['deposit_iban'])
        loan = self._get_loan(self.validated_data['loan_id'])
        with transaction.atomic():
            try:
                logger.debug(f'Starting transfer from {deposit} to {loan}')
                deposit.balance -= amount
                loan.balance -= amount
                deposit.save()
                loan.save()
            except Exception as e:
                logger.error(f'Transfer from {deposit} to {loan} failed with following exception: {e}')
                raise


class AccountToAccountTransferSerializer(TransferBaseSerializer):
    sender_account_iban = serializers.UUIDField()
    receiver_account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate_sender_account_iban(self, value):
        return self.validate_account_iban(value)

    def validate_receiver_account_iban(self, value):  # noqa
        if not BankAccount.objects.filter(iban=value).first():
            raise serializers.ValidationError(f'Wrong account provided: #{value}')
        return value

    def validate(self, attrs):
        amount = attrs['amount']
        sender_account = self._get_account(attrs['sender_account_iban'])
        receiver_account = BankAccount.objects.filter(iban=attrs['receiver_account_iban']).first()
        if sender_account.currency != receiver_account.currency:
            raise serializers.ValidationError('Currencies of the accounts do not match')
        if sender_account.balance < amount:
            raise serializers.ValidationError('Not enough balance on the account')
        return attrs

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        sender_account = self._get_account(self.validated_data['sender_account_iban'])
        receiver_account = BankAccount.objects.filter(iban=self.validated_data['receiver_account_iban']).first()
        with transaction.atomic():
            try:
                logger.debug(f'Starting transfer from {sender_account} to {receiver_account}')
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
            except Exception as e:
                logger.error(
                    f'Transfer from {sender_account} to {receiver_account} failed with following exception: {e}'
                )
                raise


class CardToAccountTransferSerializer(TransferBaseSerializer):
    debit_card_number = serializers.CharField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def _get_debit_card(self, card_number):
        return DebitCard.objects.user_cards(self._get_user_from_context()).filter(card_number=card_number).first()

    def validate_debit_card_number(self, value):
        if not self._get_debit_card(value):
            raise serializers.ValidationError(f'Wrong card number provided: #{value}')
        return value

    def validate_account_iban(self, value):  # noqa
        if not BankAccount.objects.filter(iban=value).first():
            raise serializers.ValidationError(f'Wrong account provided: #{value}')
        return value

    def validate(self, attrs):
        amount = attrs['amount']
        sender_account = self._get_debit_card(attrs['debit_card_number']).account
        receiver_account = BankAccount.objects.filter(iban=attrs['account_iban']).first()
        if sender_account.currency != receiver_account.currency:
            raise serializers.ValidationError('Currencies of the accounts do not match')
        if sender_account.balance < amount:
            raise serializers.ValidationError('Not enough balance on the account')
        return attrs

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        sender_account = self._get_debit_card(self.validated_data['debit_card_number']).account
        receiver_account = BankAccount.objects.filter(iban=self.validated_data['account_iban']).first()
        with transaction.atomic():
            try:
                logger.debug(f'Starting transfer from {sender_account} to {receiver_account}')
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
            except Exception as e:
                logger.error(
                    f'Transfer from {sender_account} to {receiver_account} failed with following exception: {e}'
                )
                raise
