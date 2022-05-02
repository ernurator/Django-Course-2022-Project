from rest_framework import serializers

from core.models import BankAccount


class BankAccountBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount


class BankAccountReadSerializer(BankAccountBaseSerializer):
    class Meta(BankAccountBaseSerializer.Meta):
        exclude = ['user']


class BankAccountWriteSerializer(BankAccountBaseSerializer):
    class Meta(BankAccountBaseSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['user']
