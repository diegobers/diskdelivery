from django.dispatch import receiver

from allauth.account.signals import user_logged_in, user_signed_up

from .models import Cart


@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    _merge_cart_user(request, user)

@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    _merge_cart_user(request, user)

def _merge_cart_user(request, user):
    session_key = request.session.session_key
    if session_key:
        try:
            cart = Cart.objects.get(session_key=session_key, user=None)
            cart.user = user
            cart.session_key = None
            cart.save()
        except Cart.DoesNotExist:
            pass