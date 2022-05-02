from django.db import transaction

from rest_framework import serializers

from core.models import BankAccount, Deposit


class DepositBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit


class DepositReadSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        exclude = ['user']


class DepositWriteSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['user', 'balance']


class DepositUpdateAmountSerializer(serializers.Serializer):
    account_iban = serializers.UUIDField()
    amount = serializers.IntegerField()

    def validate_amount(self, value):  # noqa
        if value < 0:
            raise serializers.ValidationError(f'Invalid value for amount field: {value}')
        return value

    def validate_account_iban(self, value):
        user = self.context['request'].user
        if not BankAccount.objects.user_accounts(user).filter(pk=value).first():
            raise serializers.ValidationError(f'Wrong account provided: {value}')
        return value

    def validate(self, attrs):
        account = BankAccount.objects.get(pk=attrs['account_iban'])
        if account.balance < attrs['amount']:
            raise serializers.ValidationError('Not enough balance on the account')
        return attrs

    def update(self, instance, validated_data):
        amount = validated_data['amount']
        account = BankAccount.objects.get(pk=validated_data['account_iban'])
        if account.currency != instance.currency:
            raise serializers.ValidationError('Currencies of the account and the deposit do not match')
        with transaction.atomic():
            account.balance -= amount
            instance.balance += amount
            account.save()
            instance.save()
        return instance

    def create(self, validated_data):
        raise NotImplemented
