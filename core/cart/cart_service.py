import json
from django.contrib.auth import get_user_model
from shop.models import Product
from . import exceptions
from django.core.cache import cache

# get custom user model
User = get_user_model()


class CartService:
    @staticmethod
    def get_cart_key(user_id: int) -> str:
        """
        Generate the cart key for a user.
        """
        return f"cart:{user_id}"

    @staticmethod
    def add_item(user: User, product: Product, quantity: int) -> dict:
        """
        Add an item to the user's cart; if it exists, increment.
        If it's more than product.inventory, raise an error.
        """
        if quantity > product.inventory:
            raise exceptions.MaximumQuantityExceeded(
                "The requested quantity exceeds the available inventory."
            )

        cart_key = CartService.get_cart_key(user.id)
        cart_item = cache.get(cart_key)

        if cart_item:
            cart_item = json.loads(cart_item)
            if str(product.id) in cart_item:
                if (
                    cart_item[str(product.id)]["quantity"] + quantity
                    > product.inventory
                ):
                    raise exceptions.MaximumQuantityExceeded(
                        "The requested quantity exceeds the available inventory."
                    )
                cart_item[str(product.id)]["quantity"] += quantity
                cart_item[str(product.id)]["total_price"] = str(
                    float(cart_item[str(product.id)]["price"])
                    * cart_item[str(product.id)]["quantity"]
                )
            else:
                cart_item[str(product.id)] = {
                    "title": product.title,
                    "quantity": quantity,
                    "price": str(product.final_price),
                    "total_price": str(product.final_price * quantity),
                }
        else:
            cart_item = {
                str(product.id): {
                    "title": product.title,
                    "quantity": quantity,
                    "price": str(product.final_price),
                    "total_price": str(product.final_price * quantity),
                }
            }

        cache.set(cart_key, json.dumps(cart_item), timeout=172800)
        return cart_item

    @staticmethod
    def update_item(user: User, product: Product, quantity: int) -> dict:
        """
        Update the quantity of a product in the user's cart.
        If the product is not in the cart, raise ProductNotInCart.
        If the quantity exceeds the inventory, raise MaximumQuantityExceeded.
        """
        if quantity > product.inventory:
            raise exceptions.MaximumQuantityExceeded(
                "The requested quantity exceeds the available inventory."
            )

        cart_key = CartService.get_cart_key(user.id)
        cart_item = cache.get(cart_key)

        if not cart_item:
            raise exceptions.ProductNotInCart("The product is not in your cart.")

        try:
            cart_item = json.loads(cart_item)
        except json.JSONDecodeError:
            raise exceptions.InvalidCart("The cart data is invalid.")

        if str(product.id) not in cart_item:
            raise exceptions.ProductNotInCart("The product is not in your cart.")

        if quantity <= 0:
            # If quantity is zero or negative, remove the product from the cart
            del cart_item[str(product.id)]
        else:
            cart_item[str(product.id)]["quantity"] = quantity
            cart_item[str(product.id)]["total_price"] = str(
                float(cart_item[str(product.id)]["price"]) * quantity
            )

        cache.set(cart_key, json.dumps(cart_item), timeout=172800)
        return cart_item

    @staticmethod
    def get_items(user: User) -> dict:
        """
        Get all items in the user's cart.
        If the cart is empty, return an empty dictionary.
        """
        cart_key = CartService.get_cart_key(user.id)
        cart_item = cache.get(cart_key)

        if not cart_item:
            return {}

        return json.loads(cart_item)

    @staticmethod
    def remove_item(user: User, product: Product) -> None:
        """
        Remove a product from the user's cart.
        If the product is not in the cart, raise ProductNotInCart.
        """
        cart_key = CartService.get_cart_key(user.id)
        cart_item = cache.get(cart_key)

        if not cart_item:
            raise exceptions.ProductNotInCart("The product is not in your cart.")

        cart_item = json.loads(cart_item)
        if str(product.id) not in cart_item:
            raise exceptions.ProductNotInCart("The product is not in your cart.")

        del cart_item[str(product.id)]
        cache.set(cart_key, json.dumps(cart_item), timeout=172800)

    @staticmethod
    def clear_cart(user: User) -> None:
        """
        Clear all items from the user's cart.
        """
        cart_key = CartService.get_cart_key(user.id)
        cache.delete(cart_key)
