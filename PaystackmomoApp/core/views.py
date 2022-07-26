from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from .forms import PaymentForms
from .models import Payment
# Create your views here.


def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        paymentform = PaymentForms(request.POST)
        if paymentform.is_valid():
            payment = paymentform.save()
            return render(request, 'make_payment.html', {
                'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        paymentform = PaymentForms()
        return render(request, 'initiate_payment.html', {
            'paymentform': paymentform})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_paymrnt()

    if verified:
        messages.success(request, "verification successful")
    else:
        messages.error(request, 'verification failed')
    return redirect('initiate payment')
