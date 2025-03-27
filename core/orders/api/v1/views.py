from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderCreateSerializer, OrderDetailSerializer
from django.db import transaction
from cart.cart_service import CartService
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from ...models import Order, OrderItem
from shop.models import Product
from payments.models import Payment
from payments.tasks import process_payment_task
from django.shortcuts import get_object_or_404


@method_decorator(never_cache, name="dispatch")
class OrderCreateView(CreateAPIView):

    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):

        try:
            user = self.request.user
            cart = CartService.get_items(user=user)

            if not cart:
                return Response(
                    {"detail": "Your shopping cart is empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            total_price = 0.0
            order_items_data = []
            for product_id, item_data in cart.items():
                product = get_object_or_404(Product, id=product_id)
                if product.inventory < item_data["quantity"]:
                    raise ValueError(f"Insufficient product inventory {product.title}")
                total_price += float(item_data["total_price"])
                order_items_data.append(
                    {
                        "product": product,
                        "quantity": int(item_data["quantity"]),
                        "price": float(item_data["price"]),
                    }
                )

            order = Order.objects.create(
                user=request.user, total_price=total_price, **serializer.validated_data
            )

            order_items = [
                OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"],
                )
                for item in order_items_data
            ]
            OrderItem.objects.bulk_create(order_items)

            payment = Payment.objects.create(order=order, amount=total_price)

            CartService.clear_cart(user=user)

            process_payment_task(payment_id=payment.id)

            return Response(
                OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED
            )

        except Exception:
            return Response(
                {"detail": "Error creating order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
