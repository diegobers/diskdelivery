from django.urls import path
from checkout.views import OrderConfirmationView

app_name = 'checkout'

urlpatterns = [  
    path('pedido-confirmado/', OrderConfirmationView.as_view(), name='order-confir'),
]