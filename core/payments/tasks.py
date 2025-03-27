from celery import shared_task
from django.conf import settings
from django.urls import reverse
from payments.models import Payment
from .gateways import ZibalClient
from .exceptions import PaymentError
from orders.tasks import fulfill_order_task
import logging

logger = logging.getLogger("payments")


# @shared_task(bind=True, max_retries=3)
def process_payment_task(payment_id):

    try:
        payment = Payment.objects.get(id=payment_id)
        if payment.status != "pending":
            logger.warning(f"Payment {payment_id} is not in PENDING status")
            return

        order = payment.order
        callback_url = settings.BASE_URL + reverse("payments:verify-payment")

        zibal = ZibalClient(
            merchant_id=settings.ZIBAL_MERCHANT_ID, sandbox=settings.ZIBAL_SANDBOX
        )

        amount = int(float(payment.amount))

        response = zibal.payment_request(
            amount=amount,
            callback_url=callback_url,
            description=f"Payment for order #{order.id}",
            mobile=order.phone,
            order_id=str(order.id),
        )

        track_id = response.get("trackId")
        payment_url = zibal.generate_payment_url(track_id)

        payment.transaction_id = track_id
        payment.payment_url = payment_url
        payment.gateway_response = response
        payment.save()

        logger.info(
            f"Payment {payment_id} processed successfully. Track ID: {track_id}"
        )

    except PaymentError as e:
        logger.error(f"Payment processing failed for {payment_id}: {str(e)}")
        payment.status = "FAILED"
        payment.gateway_response = {"error": str(e)}
        payment.save()
        raise  # self.retry(exc=e, countdown=60)

    except Exception as e:
        logger.exception(f"Unexpected error processing payment {payment_id}")
        payment.status = "FAILED"
        payment.gateway_response = {"error": str(e)}
        payment.save()
        raise  # self.retry(exc=e, countdown=60)


@shared_task
def verify_payment_task(track_id):

    try:
        payment = Payment.objects.get(transaction_id=track_id)
        if payment.status == "PAID":
            logger.info(f"Payment with track ID {track_id} is already verified")
            return

        zibal = ZibalClient(
            merchant_id=settings.ZIBAL_MERCHANT_ID, sandbox=settings.ZIBAL_SANDBOX
        )

        response = zibal.payment_verify(track_id)

        if response.get("result") == 100:
            payment.status = "PAID"
            payment.gateway_response = response
            payment.save()

            logger.info(f"Payment {payment.id} verified successfully")

            fulfill_order_task.delay(payment.order.id)

        else:
            payment.status = "FAILED"
            payment.gateway_response = response
            payment.save()
            logger.error(f"Payment verification failed for track ID {track_id}")

    except Payment.DoesNotExist:
        logger.error(f"Payment with track ID {track_id} not found")

    except Exception:
        logger.exception(f"Error verifying payment with track ID {track_id}")
        raise
