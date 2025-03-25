from django.db import models
from orders.models import Order

# Create your models here.

class Payment(models.Model):
    
    STATUS_CHOICES = (
        ('PENDING', 'pending'),
        ('PAID',  'paid'),
        ('FAILED', 'failed'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_url = models.URLField(blank=True, null=True)  
    gateway_response = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Payment {self.id} for order {self.order.id}'