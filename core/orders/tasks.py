from celery import shared_task
from .models import Order
from mail_templated import EmailMessage
from django.conf import settings


@shared_task
def fulfill_order_task(self, order_id):
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
    email_message = EmailMessage(
        email_message="your order registered",
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    email_message.send()