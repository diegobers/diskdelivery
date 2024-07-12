from django.db import models

from store.models import Product

class Order(models.Model):
    ORDER_STATUS  = [
        ('received','Recebido'),
        ('inprogress','Preparando'),
        ('delivered','Entregue'),
        ('canceled','Cancelado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('csh', 'Dinheiro'),
        ('cre', 'Crédito'),
        ('deb', 'Débito'),
        ('pix','Pix'),
    ]
    total = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    observation = models.TextField(blank=True, null=True)
    is_shipping = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=25, blank=True, null=True, default='')
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD_CHOICES, default='csh')
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='received')

    class Meta:
        ordering = ['-created_at']

        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()