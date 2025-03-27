from rest_framework import serializers
from ...models import Order, OrderItem
from payments.models import Payment
from shop.api.v1.serializers import ProductSerializer


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
            "transaction_id",
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
