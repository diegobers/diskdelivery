from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from .models import Cart

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        self._update_cart_user_field(request, user)
        return user

    def _update_cart_user_field(self, request, user):
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key, user=None)
                cart.user = user
                cart.session_key = None
                cart.save()
            except Cart.DoesNotExist:
                pass

