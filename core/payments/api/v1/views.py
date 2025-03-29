from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ...models import Payment
from ...tasks import verify_payment_task, process_payment_task
from .serializers import OrderCreateSerializer, OrderDetailSerializer, PaymentSerializer, PaymentRelatedSerializer
from cart.cart_service import CartService
from orders.models import Order, OrderItem
from shop.models import Product


class PaymentRequestView(CreateAPIView):

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

            process_payment_task.delay(payment_id=payment.id)

            payment.refresh_from_db()
            order.refresh_from_db()

            return Response(
                OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED
            )

        except Exception:
            return Response(
                {"detail": "Error creating order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class PaymentVerifyView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authority = serializer.validated_data.get("authority")
        
        try:
            payment = (Payment.objects.select_for_update().select_related('order').get(authority=authority, order__user=request.user))

            if payment.status == "paid":
                return Response({'detail': 'Payment already verified'}, status=status.HTTP_208_ALREADY_REPORTED)

            if not payment.authority or not payment.amount:
                raise ValidationError('Invalid payment data')

            verify_payment_task.delay(authority=payment.authority)

            payment.refresh_from_db()
            result = PaymentRelatedSerializer(payment)

            return Response(result.data, status=status.HTTP_200_OK)


        except Payment.DoesNotExist:
            return Response(
                {'detail': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {'detail': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )