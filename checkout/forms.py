from django import forms
from .models import Order

from django.utils.translation import gettext_lazy as _
from django_bootstrap5.widgets import RadioSelectButtonGroup

 
class OrderCheckoutForm(forms.ModelForm):
    SHIPPING_CHOICES = [
        (True, 'Entregar'),
        (False, 'Buscar')
    ]

    is_shipping = forms.ChoiceField(choices=SHIPPING_CHOICES, widget=RadioSelectButtonGroup)

    class Meta:
        model = Order
        fields = ['is_shipping', 'shipping_address', 'payment_method', 'observation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_shipping'].initial = True
        self.fields['is_shipping'].widget.attrs.update({'class': 'form-check-input shadow'})
        self.fields['shipping_address'].widget.attrs.update({'class': 'form-control shadow'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control shadow'})
        self.fields['observation'].widget.attrs.update({'class': 'form-control shadow'})

        self.fields['shipping_address'].label = _('Endereço')
        self.fields['payment_method'].label = _('Pagamento')

    def clean(self):
        cleaned_data = super().clean()
        is_shipping = cleaned_data.get('is_shipping') == 'True'
        shipping_address = cleaned_data.get('shipping_address')
        payment_method = cleaned_data.get('payment_method')
        observation = cleaned_data.get('observation')

        if is_shipping:
            self.fields['shipping_address'].required = True
            if not shipping_address:
                self.add_error('shipping_address', _('Informar endereço de entrega!'))
        else:
            self.fields['shipping_address'].required = False

        return cleaned_data