from celery import shared_task
from payments.gateways import ZibalPaymentGateway
from payments.models import Payment

@shared_task(bind=True, max_retries=3)
def process_payment_task(self, payment_id):
    pass

@shared_task
def verify_payment_task(payment_id):
    pass 