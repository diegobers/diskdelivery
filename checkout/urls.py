from django.urls import path
from checkout.views import OrderConfirmationView, OrdersView, OrderDetail

app_name = 'checkout'


urlpatterns = [  
    path('pedido-confirmado/', OrderConfirmationView.as_view(), name='order-confir'),
    path('seus-pedidos/', OrdersView.as_view(), name='orders'),
    path('detalhes/<int:pk>/', OrderDetail.as_view(), name='order_view'),
]