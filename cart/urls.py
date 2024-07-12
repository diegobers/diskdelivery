from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [  
    path('seu-carrinho/', views.CartView.as_view(), name='view_cart'),
    path('adicionar/', views.AddProductCartView.as_view(), name='add_product'),
    path('limpar-carrinho/', views.CleanCartView.as_view(), name='clean_cart'),
]