from django.shortcuts import render
from django.urls import reverse_lazy

from allauth.account.views import LoginView
from allauth.account.views import SignupView

from cart.models import Cart

from .forms import CustomSignupForm

class LoginOnGetView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('store:index') 
    
    def get(self, request, *args, **kwargs):
        request.session['last_session_key'] = request.session.session_key
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        last_session_key = self.request.session.get('last_session_key')
        cart_queryset = Cart.objects.filter(session_key=last_session_key)

        if cart_queryset.exists():
            cart = cart_queryset.first()
            cart.user_id = self.request.user.id
            cart.session_key = None
            cart.save()
            del self.request.session['last_session_key']
            #messages.success(request, ("Update Cart Items..."))
        return response

class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('checkout:orders')
    
    def get(self, request, *args, **kwargs):
        request.session['last_session_key'] = request.session.session_key
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        last_session_key = self.request.session.get('last_session_key')
        cart_queryset = Cart.objects.filter(session_key=last_session_key)
        if cart_queryset.exists():
            cart = cart_queryset.first()
            cart.user_id = self.request.user.id
            cart.session_key = None
            cart.save()
        return response