from django import forms
from .models import Payment


class PaymentForms(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('email', 'amount')
