from django.db import models
 
from store.models import Gas


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    @property
    def get_cart_total(self):
        total = sum(prod.get_cart_item_subtotal for prod in self.prods.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Gas, related_name='prods', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Gas, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    
    @property
    def get_cart_item_subtotal(self):
        return self.product.price * self.quantity