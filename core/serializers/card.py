from rest_framework import serializers

from core.models import DebitCard
from .account import BankAccountReadSerializer


class DebitCardBaseSerializer(serializers.ModelSerializer):
    account = BankAccountReadSerializer

    class Meta:
        model = DebitCard

    def validate_account(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError('Wrong account provided')
        return value


class DebitCardReadSerializer(DebitCardBaseSerializer):
    class Meta(DebitCardBaseSerializer.Meta):
        fields = '__all__'
        depth = 1


class DebitCardWriteSerializer(DebitCardBaseSerializer):
    class Meta(DebitCardBaseSerializer.Meta):
        fields = '__all__'


class DebitCardUpdateSerializer(DebitCardBaseSerializer):
    class Meta(DebitCardBaseSerializer.Meta):
        fields = ['account']
