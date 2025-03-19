from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        validate_data["phone"] = self.user.phone
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.pk
        return validate_data

class OtpRequestSerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=11, required=True)

    def validate(self, attrs):
        if not attrs.get("phone").isdigit():
            raise serializers.ValidationError({"detail":"Invalid phone number."})
        if not attrs.get("phone").startswith("09"):
            raise serializers.ValidationError({"detail":"Phone must start with 09 digits."})
        return super().validate(attrs)

class OtpVerifySerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=11, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        if not attrs.get("phone").isdigit():
            raise serializers.ValidationError({"detail":"Invalid phone number."})
        if not attrs.get("phone").startswith("09"):
            raise serializers.ValidationError({"detail":"Phone must start with 09 digits."})
        return super().validate(attrs)