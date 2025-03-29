from rest_framework import serializers 
from ...models import Order, OrderItem
from shop.api.v1.serializers import ProductSerializer
from payments.models import Payment

class OrderItemRelatedSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "id", 
            "product",
            "quantity",
            "price",
        ]

class PaymentOrderRelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id", 
            "status",
            "amount",
            "gateway_response",
            "created"
        ]


class ShopUserOrdersRelatedSerializer(serializers.ModelSerializer):
    
    items = OrderItemRelatedSerializer(many=True)
    payment = PaymentOrderRelatedSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "address",
            "postal_code",
            "province",
            "city",
            "total_price",
            "status",
            "items",
            "payment",
            "created"
        ] 