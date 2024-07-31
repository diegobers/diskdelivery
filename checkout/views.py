from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .models import Order, OrderItem

class OrderConfirmationView(LoginRequiredMixin, CreateView):
    template_name = 'checkout/order_confirmation.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_queryset()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).last()

class OrdersView(LoginRequiredMixin, ListView):
    template_name = 'checkout/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_queryset()

        for order in orders:
            order.order_items = OrderItem.objects.filter(order=order)

        return context