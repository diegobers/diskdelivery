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
    context_object_name = 'cart'
    form_class = OrderCheckoutForm
    success_url = reverse_lazy('store:order-confir')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).last()
        else:
            cart = Cart.objects.filter(session_key=self.request.session.session_key).last()
        
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object() if self.get_object() else None
        context['cart_items'] = CartItem.objects.filter(cart=cart) if cart else []
        context['cart_total'] = cart.get_cart_total if cart else 0
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
            total=cart.get_cart_total        )
        
        for item in cart.prods.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        
        cart.prods.all().delete()
        cart.delete()
        
        return super().form_valid(form)

class CartView2(FormView, DetailView):
    template_name = 'cart/items.html'
    context_object_name = 'cart'
    form_class = OrderCheckoutForm
    success_url = reverse_lazy('store:order-confir')
    def get_object(self):
        if self.request.user.is_authenticated:
            return Cart.objects.get(user=self.request.user)
        elif self.request.user.is_anonymous:
            return Cart.objects.get(session_key=self.request.session.session_key)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object().last() if self.get_object() else None
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        context['cart_total'] = cart.get_cart_total if cart else 0
        context['form'] = self.get_form()
        return context
    def form_valid(self, form):
        cart = self.get_object()
        order = Order.objects.create(
            shipping_address=form.cleaned_data['shipping_address'] if form.cleaned_data['is_shipping'] == 'True' else None,
            payment_method=form.cleaned_data['payment_method'],
            observation=form.cleaned_data['observation'],
            is_shipping=form.cleaned_data['is_shipping'],
            total=sum(item.product.price * item.quantity for item in cart.prods.all())        
        )   
        for item in cart.prods.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
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

        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart:view_cart')