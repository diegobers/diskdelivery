from django.urls import path
from checkout.views import OrderConfirmationView, OrdersView

app_name = 'checkout'


urlpatterns = [  
    path('pedido-confirmado/', OrderConfirmationView.as_view(), name='order-confir'),
    path('seus-pedidos/', OrdersView.as_view(), name='orders'),
]