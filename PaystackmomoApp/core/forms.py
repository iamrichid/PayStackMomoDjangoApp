from django import forms
# from .models import 


class PaymentForms(forms.ModelForm):
    class Meta:
        # model = 
        fields = ('email', 'amount')
