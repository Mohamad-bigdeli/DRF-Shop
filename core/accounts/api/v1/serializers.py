from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from ...models import Profile

# get custom user model 
User = get_user_model()

class ShopUserRelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["phone", "email", "is_verified", "created", "updated"]

class ShopUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["phone", "email", "is_verified", "created", "updated"]
        read_only_fields = ["phone", "is_verified", "created", "updated"]

class ShopUserRegisterSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["phone", "email", "password", "password1", "is_verified", "created", "updated"]
        read_only_fields = ["is_verified", "created", "updated"]
    
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail":"passwords doesn't match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)

class ShopUserChangePasswordSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(max_length=255, required=True) 
    new_password = serializers.CharField(max_length=255, required=True) 
    new_password1 = serializers.CharField(max_length=255, required=True) 

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"derail":"passwords doesn't match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

class ShopUserForgotPasswordEmailSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255, required=True)

class ShopUserForgotPasswordPhoneSerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=11, required=True)

    def validate(self, attrs):
        if not attrs.get("phone").isdigit():
            raise serializers.ValidationError({"detail":"Invalid phone number."})
        if not attrs.get("phone").startswith("09"):
            raise serializers.ValidationError({"detail":"Phone must start with 09 digits."})
        return super().validate(attrs)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255 ,required=False)
    phone = serializers.CharField(max_length=11, required=False)
    verification_code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(max_length=255, required=True)
    new_password1 = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("phone"):
            raise serializers.ValidationError("Either email or phone number is required.")
        if attrs.get("email"):
            try:
                user = User.objects.filter(email=attrs.get("email"))
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")
        if attrs.get("phone"):
            if not attrs.get("phone").isdigit():
                raise serializers.ValidationError({"detail":"Invalid phone number."})
            if not attrs.get("phone").startswith("09"):
                raise serializers.ValidationError({"detail":"Phone must start with 09 digits."})
            try:
                user = User.objects.filter(phone=attrs.get("phone"))
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this phone number does not exist.")
        return super().validate(attrs)

class ProfileRelatedSerializer(serializers.ModelSerializer):

    user = ShopUserRelatedSerializer()
    class Meta:
        model = Profile
        fields = [
            "user",
            "first_name",
            "last_name",
            "bio",
            "address",
            "postal_code",
            "image",
            "created",
            "updated"
        ]
        read_only_fields = ["__all__"]

class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "bio",
            "address",
            "postal_code",
            "image",
        ]
