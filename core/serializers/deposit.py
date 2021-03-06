from rest_framework import serializers

from core.models import Deposit


class DepositBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit


class DepositReadSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        exclude = ['user']


class DepositCreateSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        fields = ['currency', 'user', 'balance', 'due_date', 'rate', 'iban']
        read_only_fields = ['user', 'balance', 'due_date', 'iban']
