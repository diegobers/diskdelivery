from django.db import models


class Agua(models.Model):
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.description

class Gas(models.Model):
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.description