from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderCreateSerializer, OrderDetailSerializer
from django.db import transaction
from cart.cart_service import CartService
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from ...services import OrderService

@method_decorator(never_cache, name='dispatch')
class OrderCreateView(CreateAPIView):

    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        
        try:
            user = self.request.user
            cart = CartService.get_items(user=user)

            if not cart:
                return Response({"detail":"Your shopping cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            order = OrderService.create_order(
                user=user,
                cart_items=cart,
                shipping_data=serializer.validated_data
            )

            CartService.clear_cart(user=user)

            return Response(
                OrderDetailSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {"detail": "Error creating order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
