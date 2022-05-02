from rest_framework import serializers

from core.models import DebitCard
from .account import BankAccountReadSerializer


class DebitCardBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebitCard

    def validate_account(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(f'Wrong account provided: {value}')
        return value


class DebitCardReadSerializer(DebitCardBaseSerializer):
    account = BankAccountReadSerializer

    class Meta(DebitCardBaseSerializer.Meta):
        fields = '__all__'
        depth = 1


class DebitCardWriteSerializer(DebitCardBaseSerializer):
    class Meta(DebitCardBaseSerializer.Meta):
        fields = '__all__'


class DebitCardUpdateSerializer(DebitCardBaseSerializer):
    class Meta(DebitCardBaseSerializer.Meta):
        fields = ['account']
