from django.db import transaction

from rest_framework import serializers

from core.models import BankAccount, Deposit


class AccountToDepositTransferSerializer(serializers.Serializer):
    deposit_iban = serializers.UUIDField()
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField()

    def _get_user_from_context(self):
        return self.context['request'].user

    def _get_deposit(self, iban):
        return Deposit.objects.user_deposits(self._get_user_from_context()).filter(iban=iban).first()

    def _get_account(self, iban):
        return BankAccount.objects.user_accounts(self._get_user_from_context()).filter(iban=iban).first()

    def validate_deposit_iban(self, value):
        if not self._get_deposit(value):
            raise serializers.ValidationError(f'Wrong deposit provided: #{value}')
        return value

    def validate_account_iban(self, value):
        if not self._get_account(value):
            raise serializers.ValidationError(f'Wrong account provided: #{value}')
        return value

    def validate_amount(self, value):  # noqa
        if value < 0:
            raise serializers.ValidationError(f'Invalid value for amount field: {value}')
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

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
