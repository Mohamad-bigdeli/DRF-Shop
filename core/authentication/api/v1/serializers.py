from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        validate_data["phone"] = self.user.phone
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.pk
        return validate_data