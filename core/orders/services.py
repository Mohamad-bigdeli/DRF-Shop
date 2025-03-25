from django.db import transaction
from .models import Order, OrderItem
from shop.models import Product
from payments.models import Payment
from .tasks import process_payment_task

class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user, cart_items, shipping_data):

        total_price = 0
        order_items_data = []
        
        for product_id, item_data in cart_items.items():
            product = Product.objects.select_for_update().get(pk=product_id)
            quantity = item_data['quantity']
            
            if product.inventory < quantity:
                raise ValueError(f"Insufficient product inventory {product.title}")
            
            unit_price = float(item_data['price'])
            total_price += unit_price * quantity
            
            order_items_data.append({
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price
            })

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            **shipping_data
        )

        order_items = [
            OrderItem(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            ) for item in order_items_data
        ]
        OrderItem.objects.bulk_create(order_items)

        payment = Payment.objects.create(
            order=order,
            amount=total_price
        )

        process_payment_task.delay(payment.id)

        return order