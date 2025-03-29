from celery import shared_task
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from payments.models import Payment
from .gateways.zarinpal import ZarinPalClient
from .exceptions import PaymentError
from orders.tasks import fulfill_order_task, send_order_email
import logging

logger = logging.getLogger("payments")

@transaction.atomic()
@shared_task
def process_payment_task(self, payment_id):

    """
    Processes payment request through ZarinPal gateway:
    - Creates payment request in gateway
    - Stores gateway response
    - Handles retries for failed attempts
    """

    try:
        payment = Payment.objects.get(id=payment_id)
        if payment.status != "pending":
            logger.warning(f"Payment {payment_id} is not in PENDING status")
            return

        order = payment.order
        callback_url = settings.BASE_URL + reverse("orders:api-v1:user-orders")

        zarinpal = ZarinPalClient(
            merchant_id=settings.ZARINPAL_MERCHANT_ID, sandbox=settings.ZARINPAL_SANDBOX
        )

        amount = int(float(payment.amount))

        response = zarinpal.request_payment(
            amount=amount,
            callback_url=callback_url,
            description=f"Payment for order #{order.id}",
            mobile=order.phone,
        )

        authority = response.get("authority")
        payment_url = response.get("payment_url")

        payment.authority = authority
        payment.payment_url = payment_url
        payment.gateway_response = response
        payment.save()

        logger.info(
            f"Payment {payment_id} processed successfully. Track ID: {authority}"
        )

    except PaymentError as e:
        logger.error(f"Payment processing failed for {payment_id}: {str(e)}")
        payment.status = "failed"
        payment.gateway_response = {"error": str(e)}
        payment.save()
        raise  self.retry(exc=e, countdown=60)

    except Exception as e:
        logger.exception(f"Unexpected error processing payment {payment_id}")
        payment.status = "failed"
        payment.gateway_response = {"error": str(e)}
        payment.save()
        raise self.retry(exc=e, countdown=60)

@transaction.atomic()
@shared_task
def verify_payment_task(authority):

    """
    Verifies payment with ZarinPal gateway:
    - Checks payment status
    - Updates local payment record
    - Triggers order fulfillment on success
    """

    try:
        payment = Payment.objects.get(authority=authority)
        if payment.status == "paid":
            logger.info(f"Payment with authority {authority} is already verified")
            return

        zarinpal = ZarinPalClient(
            merchant_id=settings.ZARINPAL_MERCHANT_ID, sandbox=settings.ZARINPAL_SANDBOX
        )

        response = zarinpal.verify_payment(authority=authority, amount=int(float(payment.amount)))

        if response["raw_response"]["data"]["code"] == 100:  
            payment.status = "PAID"
            payment.gateway_response = response
            payment.save()
            logger.info(f"Payment {payment.id} verified successfully")
            fulfill_order_task.delay(order_id=payment.order.id)
            email = payment.order.user.email
            if email:
                send_order_email.delay(email)

        else:
            payment.status = "FAILED"
            payment.gateway_response = response
            payment.save()
            logger.error(f"Payment verification failed. ZarinPal response: {response}")


    except Payment.DoesNotExist:
        logger.error(f"Payment with authority {authority} not found")

    except Exception:
        logger.exception(f"Error verifying payment with authority {authority}")
        raise
