from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...cart_service import CartService
from rest_framework.response import Response
from shop.models import Product
from ... import exceptions

class CartViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Get all items in the user's cart.
        """
        cart_items = CartService.get_items(request.user)
        return Response(cart_items)

    def create(self, request):
        """
        Add an item to the user's cart.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_items = CartService.add_item(request.user, product, quantity)
            return Response(cart_items, status=status.HTTP_201_CREATED)
        except exceptions.MaximumQuantityExceeded as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update the quantity of a product in the user's cart.
        """
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_items = CartService.update_item(request.user, product, quantity)
            return Response(cart_items)
        except exceptions.MaximumQuantityExceeded as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ProductNotInCart as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Remove a product from the user's cart.
        """
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            CartService.remove_item(request.user, product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.ProductNotInCart as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        Clear all items from the user's cart.
        """
        CartService.clear_cart(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)