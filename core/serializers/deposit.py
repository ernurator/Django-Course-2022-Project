from rest_framework import serializers

from core.models import Deposit


class DepositBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit


class DepositReadSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        exclude = ['user']


class DepositWriteSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['user']


class DepositUpdateSerializer(DepositBaseSerializer):
    class Meta(DepositBaseSerializer.Meta):
        fields = ['balance', 'due_date', 'rate']