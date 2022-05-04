from rest_framework import serializers

from core.models import Loan


class LoanBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan


class LoanReadSerializer(LoanBaseSerializer):
    class Meta(LoanBaseSerializer.Meta):
        exclude = ['user']


class LoanCreateSerializer(LoanBaseSerializer):
    class Meta(LoanBaseSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['user']


class LoanUpdateSerializer(LoanBaseSerializer):
    class Meta(LoanBaseSerializer.Meta):
        fields = ['balance', 'rate']
