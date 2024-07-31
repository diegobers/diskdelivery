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

    def form_valid(self, form):
        cart = self.get_cart()
        if not cart:
            # Redirect to cart if no items to order
            return redirect('cart:cart-items')

        # Create the order object
        order = form.save(commit=False)
        order.user = self.request.user
        order.total = sum(item.product.price * item.quantity for item in cart.prods.all())
        order.save()

        # Transfer CartItems to OrderItems
        for cart_item in cart.prods.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )

        # Clear the cart after the order is created
        cart.prods.all().delete()
        cart.delete()
        
        self.object = order  # Set self.object to the created order

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object
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