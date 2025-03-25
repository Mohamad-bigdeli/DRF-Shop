from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

# Create your models here.

# get custom user model
User = get_user_model()

class Order(models.Model):
    
    STATUS_CHOICES = (
        ('PENDING', 'pending'),
        ('PROCESSING', 'processing'),
        ('COMPLETED', 'completed'),
        ('CANCELED', 'cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.id)
    