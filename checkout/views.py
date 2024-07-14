from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import TemplateView

from .models import Order

class OrderConfirmationView(TemplateView):
    template_name = 'checkout/order_confirmation.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_queryset()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).last()