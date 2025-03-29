from rest_framework import serializers 
from...models import Payment
from orders.models import Order, OrderItem
from shop.api.v1.serializers import ProductSerializer
from accounts.api.v1.serializers import ShopUserRelatedSerializer


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
            raise serializers.ValidationError({"detail": "Invalid phone number."})
        if not attrs.get("phone").startswith("09"):
            raise serializers.ValidationError(
                {"detail": "Phone must start with 09 digits."}
            )
        return super().validate(attrs)


class OrderPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "amount",
            "authority",
            "payment_url",
            "gateway_response",
            "created",
        ]
        read_only_fields = fields


class OrderItemsSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):

    payment = OrderPaymentSerializer()
    items = OrderItemsSerializer(many=True)
    user = ShopUserRelatedSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "payment",
            "items",
            "user",
            "first_name",
            "last_name",
            "phone",
            "address",
            "postal_code",
            "province",
            "city",
            "total_price",
            "status",
            "created",
            "updated",
        ]
        read_only_fields = fields

class PaymentRelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id", 
            "status",
            "amount",
            "authority",
            "gateway_response",
            "created"
        ]

class PaymentSerializer(serializers.Serializer):

    authority = serializers.CharField(max_length=36, required=True)