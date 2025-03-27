from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shop.models import Product
from ...cart_service import CartService
from ... import exceptions
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AddItemToCartView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add an item to the user's cart.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID of the product to add"
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Quantity of the product",
                    default=1,
                ),
            },
            required=["product_id"],
        ),
        responses={
            200: openapi.Response(
                "Item added to cart",
                examples={
                    "application/json": {
                        "1": {
                            "title": "Product 1",
                            "quantity": 2,
                            "price": "19.99",
                            "total_price": "39.98",
                        }
                    }
                },
            ),
            400: openapi.Response(
                "Bad Request",
                examples={
                    "application/json": {
                        "error": "The requested quantity exceeds the available inventory."
                    }
                },
            ),
            404: openapi.Response(
                "Not Found",
                examples={"application/json": {"error": "Product not found."}},
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        product = get_object_or_404(Product, id=product_id)

        try:
            cart_item = CartService.add_item(user, product, quantity)
            return Response(cart_item, status=status.HTTP_200_OK)
        except exceptions.MaximumQuantityExceeded as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateItemInCartView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the quantity of a product in the user's cart.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID of the product to update"
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="New quantity of the product"
                ),
            },
            required=["product_id", "quantity"],
        ),
        responses={
            200: openapi.Response(
                "Cart updated",
                examples={
                    "application/json": {
                        "1": {
                            "title": "Product 1",
                            "quantity": 3,
                            "price": "19.99",
                            "total_price": "59.97",
                        }
                    }
                },
            ),
            400: openapi.Response(
                "Bad Request",
                examples={
                    "application/json": {
                        "error": "The requested quantity exceeds the available inventory."
                    }
                },
            ),
            404: openapi.Response(
                "Not Found",
                examples={
                    "application/json": {"error": "The product is not in your cart."}
                },
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        product = get_object_or_404(Product, id=product_id)

        try:
            cart_item = CartService.update_item(user, product, quantity)
            return Response(cart_item, status=status.HTTP_200_OK)
        except exceptions.MaximumQuantityExceeded as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ProductNotInCart as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class GetCartItemsView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all items in the user's cart.",
        responses={
            200: openapi.Response(
                "Cart items",
                examples={
                    "application/json": {
                        "1": {
                            "title": "Product 1",
                            "quantity": 2,
                            "price": "19.99",
                            "total_price": "39.98",
                        },
                        "2": {
                            "title": "Product 2",
                            "quantity": 1,
                            "price": "29.99",
                            "total_price": "29.99",
                        },
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartService.get_items(user)
        return Response(cart_items, status=status.HTTP_200_OK)


class RemoveItemFromCartView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Remove an item from the user's cart.",
        manual_parameters=[
            openapi.Parameter(
                name="product_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="ID of the product to remove",
                required=True,
            )
        ],
        responses={
            204: openapi.Response("Item removed from cart"),
            404: openapi.Response(
                "Not Found",
                examples={
                    "application/json": {"error": "The product is not in your cart."}
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        product_id = request.query_params.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)

        try:
            CartService.remove_item(user, product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.ProductNotInCart as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Clear all items from the user's cart.",
        responses={
            204: openapi.Response("Cart cleared"),
        },
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        CartService.clear_cart(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
