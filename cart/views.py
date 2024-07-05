from django.shortcuts import render

from django.views.generic import (
    CreateView, 
    ListView, 
    TemplateView, 
    View
)

from store.models import Gas

from .models import Cart, CartItem


class CartView(ListView):
    model = Cart
    template_name = 'cart/items.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.objects.filter(session_key=self.request.session.session_key)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_queryset().first().cart if self.get_queryset().exists() else None
        context['cart_items'] = CartItem.objects.filter(cart=cart.id).all()
        context['cart_total'] = cart.get_cart_total if cart else 0
        return context


class CleanCartView(DeleteView):
    model = Cart
    http_method_names = ['post']
   
    def get_object(self, queryset=None):
        return Cart.objects.get(session_key=self.request.session.session_key)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.delete()
        return reverse_lazy('cart:view_cart')

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product = request.POST.get('product_id')
        product = Gas.objects.get(id=product_id)

        if not request.session.session_key:
            request.session.create()
        
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('store:view_cart')