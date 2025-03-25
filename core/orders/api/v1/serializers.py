from rest_framework import serializers
from ...models import Order

class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "first_name", 
            "last_name", 
            "phone", 
            "address",
            "postal_code",
            "province",
            "city", 
            ]
    
    def validate(self, attrs):
        if not attrs.get("phone").isdigit():
            raise serializers.ValidationError({"detail":"Invalid phone number."})
        if not attrs.get("phone").startswith("09"):
            raise serializers.ValidationError({"detail":"Phone must start with 09 digits."})
        return super().validate(attrs)

class OrderDetailSerializer(serializers.ModelSerializer):
    pass