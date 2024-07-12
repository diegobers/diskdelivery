from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from checkout.models import Order, OrderItem

from .models import Product


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        return context

class AdminDashboardView(ListView):
    model = Order
    template_name = 'layouts/admin-dashboard.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_queryset()
        for order in orders:
            order.order_items = OrderItem.objects.filter(order=order)
        context['orders'] = orders
        return context