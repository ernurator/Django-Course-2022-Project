from rest_framework import serializers

from .models import User, UserDocuments


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class UserSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        exclude = ['password']


class UserCreateSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        fields = ['username', 'password', 'phone_number', 'is_merchant', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserDocumentsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocuments


class UserDocumentsReadSerializer(UserDocumentsBaseSerializer):
    class Meta(UserDocumentsBaseSerializer.Meta):
        exclude = ['user']


class UserDocumentsCreateSerializer(UserDocumentsBaseSerializer):
    # TODO: add validation that there is no user documents for the user
    class Meta(UserDocumentsBaseSerializer.Meta):
        fields = ['passport_image']
