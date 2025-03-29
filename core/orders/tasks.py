from celery import shared_task
from .models import Order
from mail_templated import EmailMessage
from django.conf import settings


@shared_task
def fulfill_order_task(self, order_id):
    """
    Celery task to process and fulfill an order:
    - Deducts ordered items from inventory
    - Updates order status to COMPLETED
    - Auto-retries on failure with 5min delay
    """
    try:
        order = Order.objects.get(id=order_id)

        for item in order.items.all():
            product = item.product
            product.inventory -= item.quantity
            product.save()

        order.status = "COMPLETED"
        order.save()

    except Exception as e:
        raise self.retry(exec=e ,countdown=300)

@shared_task
def send_order_email(email):
    """
    Async task to send order confirmation email:
    - Uses Django's email settings
    - Sends to customer's email address
    """
    email_message = EmailMessage(
        email_message="your order registered",
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    email_message.send()