from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic.list import ListView
from django.views.generic import (
    CreateView, 
    TemplateView, 
    View,
    DeleteView,
    FormView,
    DetailView,
)

from store.models import Product
from checkout.forms import OrderCheckoutForm
from checkout.models import Order, OrderItem
from .models import Cart, CartItem


class CartView(DetailView, FormView):
    template_name = 'cart/items.html'
    form_class = OrderCheckoutForm
    success_url = reverse_lazy('checkout:order-confir')

    def get_object(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).last()
        elif self.request.user.is_anonymous:
            return Cart.objects.filter(session_key=self.request.session.session_key).last() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object() if self.get_object() else None
        context['items'] = cart.prods.all() if cart else None
        context['form'] = self.get_form()
        return context
    
    def form_valid(self, form):
        cart = self.get_object()
        if not cart:
            return self.form_invalid(form)

        order = Order.objects.create(
            user=self.request.user,
            shipping_address=form.cleaned_data['shipping_address'] if form.cleaned_data['is_shipping'] == 'True' else None,
            payment_method=form.cleaned_data['payment_method'],
            observation=form.cleaned_data['observation'],
            is_shipping=form.cleaned_data['is_shipping'],
        )  

        # Transfer CartItems to OrderItems
        for cart_item in cart.prods.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )

        # Clear the cart after order is created
        cart.prods.all().delete()
        cart.delete()

        return super().form_valid(form)

class CleanCartView(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart:view_cart')

    def get_object(self, queryset=None):
        return Cart.objects.get(session_key=self.request.session.session_key)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.delete()
        success_url = self.get_success_url()
        return redirect(success_url)

class AddProductCartView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('product_id')
        product = Product.objects.get(id=id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart:view_cart')