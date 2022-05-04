import logging

from django.db import transaction

from rest_framework import serializers

from core.models import Loan, BankAccount

logger = logging.getLogger(__name__)


class LoanBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan


class LoanReadSerializer(LoanBaseSerializer):
    class Meta(LoanBaseSerializer.Meta):
        fields = ['id', 'currency', 'balance', 'rate']


class LoanCreateSerializer(LoanBaseSerializer):
    account_iban = serializers.UUIDField(write_only=True)

    class Meta(LoanBaseSerializer.Meta):
        fields = ['currency', 'balance', 'rate', 'account_iban', 'id']

    def _get_user_from_context(self):
        return self.context['request'].user

    def _get_account(self, iban):
        return BankAccount.objects.get_user_account(user=self._get_user_from_context(), iban=iban)

    def validate_account_iban(self, value):
        if not self._get_account(value):
            raise serializers.ValidationError(f'Wrong account provided: {value}')
        return value

    def validate(self, attrs):
        account = self._get_account(attrs['account_iban'])
        if account.currency != attrs['currency']:
            raise serializers.ValidationError('Currencies of the account and the loan do not match')
        return attrs

    def create(self, validated_data):
        account_iban = validated_data.pop('account_iban')
        with transaction.atomic():
            try:
                logger.debug(
                    f"Creating loan [{validated_data['balance']} {validated_data['currency']}], "
                    "transferring money to account #{account_iban}"
                )
                instance = super().create(validated_data)
                account = self._get_account(account_iban)
                account.balance += instance.balance
                account.save()
            except Exception as e:
                logger.error(f'Creating loan failed with following exception: {e}')
                raise
        return instance
