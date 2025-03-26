from celery import shared_task
from .models import Order

@shared_task(bind=True, max_retries=3)
def fulfill_order_task(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        for item in order.items.all():
            product = item.product
            product.inventory -= item.quantity
            product.save()
        
        order.status = 'PROCESSING'
        order.save()
        
    except Exception as e:
        raise self.retry(exc=e, countdown=300)