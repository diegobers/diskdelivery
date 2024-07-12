from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    CreateView, 
    ListView, 
    TemplateView, 
    View,
    DeleteView,
)

from store.models import Product

from .models import Cart, CartItem


class CartView(ListView):
    model = Cart
    template_name = 'cart/items.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.objects.filter(session_key=self.request.session.session_key)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_queryset().first() if self.get_queryset().exists() else None
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        context['cart_total'] = cart.get_cart_total if cart else 0
        return context


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