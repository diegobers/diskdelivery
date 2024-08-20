from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse


from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from cart.models import Cart, CartItem

from .models import Order, OrderItem

class OrderConfirmationView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'checkout/order_confirmation.html'
    fields = []
    context_object_name = 'order'
    success_url = reverse_lazy('checkout:order-confir')

    def get_cart(self):
        return Cart.objects.filter(user=self.request.user).last()

    def get_object(self):
        """Retrieve the last order created by the user or create a new one."""
        # Try to get the latest order for the user
        order = Order.objects.filter(user=self.request.user).last()
        if order:
            return order
        
        cart = self.get_cart()
        if not cart:
            return None

        order = Order.objects.create(
            user=self.request.user,
            total=sum(item.product.price * item.quantity for item in cart.prods.all()),
            shipping_address=form.cleaned_data['shipping_address'] if form.cleaned_data['is_shipping'] == 'True' else None,
            payment_method=form.cleaned_data['payment_method'],
            observation=form.cleaned_data['observation'],
            is_shipping=form.cleaned_data['is_shipping'],
        )  

        for cart_item in cart.prods.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )
        cart.prods.all().delete()
        cart.delete()
        
        return order

    def form_valid(self, form):
        self.object = self.get_object()
        if not self.object:
            return redirect('cart:view_cart')

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order'] = order
        context['items'] = order.items.all() if order else None
        return context



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