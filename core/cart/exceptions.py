class CartException(Exception):
    """
    Base exception for all cart-related errors.
    """

    pass


class MaximumQuantityExceeded(CartException):
    """
    Raised when the quantity of a product exceeds the maximum allowed per order.
    """

    def __init__(self, message="The quantity exceeds the maximum allowed per order."):
        self.message = message
        super().__init__(self.message)


class ProductNotInCart(CartException):
    """
    Raised when a product is not found in the user's cart.
    """

    def __init__(self, message="The product is not in the cart."):
        self.message = message
        super().__init__(self.message)


class ProductUnavailable(CartException):
    """
    Raised when a product is not available for purchase.
    """

    def __init__(self, message="The product is currently unavailable."):
        self.message = message
        super().__init__(self.message)
