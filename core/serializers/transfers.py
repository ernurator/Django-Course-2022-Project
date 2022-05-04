from django.db import transaction
from django.core.validators import MinValueValidator

from rest_framework import serializers

from core.models import BankAccount, Deposit, Loan


class TransferBaseSerializer(serializers.Serializer):
    def _get_user_from_context(self):
        return self.context['request'].user

    def _get_account(self, iban):
        return BankAccount.objects.get_user_account(user=self._get_user_from_context(), iban=iban)

    def _get_deposit(self, iban):
        return Deposit.objects.get_user_deposit(user=self._get_user_from_context(), iban=iban)

    def _get_loan(self, id_):
        return Loan.objects.get_user_loan(user=self._get_user_from_context(), id_=id_)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AccountToDepositTransferSerializer(TransferBaseSerializer):
    deposit_iban = serializers.UUIDField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate_deposit_iban(self, value):
        if not self._get_deposit(value):
            raise serializers.ValidationError(f'Wrong deposit provided: #{value}')
        return value

    def validate_account_iban(self, value):
        if not self._get_account(value):
            raise serializers.ValidationError(f'Wrong account provided: #{value}')
        return value

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
            account.balance -= amount
            deposit.balance += amount
            account.save()
            deposit.save()


class AccountToLoanTransferSerializer(TransferBaseSerializer):
    loan_id = serializers.IntegerField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField(validators=[MinValueValidator(0.0)])

    def validate_loan_id(self, value):
        if not self._get_loan(value):
            raise serializers.ValidationError(f'Wrong loan id provided: #{value}')
        return value

    def validate_account_iban(self, value):
        if not self._get_account(value):
            raise serializers.ValidationError(f'Wrong account provided: #{value}')
        return value

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
            account.balance -= amount
            loan.balance -= amount
            account.save()
            loan.save()
