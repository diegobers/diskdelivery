from django.db import models


class Product(models.Model):
    CATEGORY = {
        "A": "Agua",
        "G": "Gas", 
    }
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.CharField(max_length=1, choices=CATEGORY)
    
    def __str__(self):
        return self.description