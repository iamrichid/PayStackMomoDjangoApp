from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from .forms import PaymentForms
from .models import Payment
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer, PaymentSerializer,PaymentVerificationSerializer

# Create your views here.



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer    


class VerifyPayment(APIView):
    
    def post(self, request, ref):
        payment = PaymentVerificationSerializer(ref=ref)
        # payment = get_object_or_404(Payment, ref=ref)
        verified = payment.verify_payment()
        if verified:
            messages.success(request, "verification successful")
        else:
            messages.error(request, 'verification failed')
        return redirect('initiate payment')


def initiate_payment(request):
    if request.method == "POST":
        paymentform = PaymentForms(request.POST)
        if paymentform.is_valid():
            payment = paymentform.save()
            return render(request, 'make_payment.html', {
                'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        paymentform = PaymentForms()
        return render(request, 'initiate_payment.html', {
            'paymentform': paymentform})


def verify_payment(request, ref:str):
    print(ref)
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()

    if verified:
        messages.success(request, "verification successful")
    else:
        messages.error(request, 'verification failed')
    return redirect('initiate payment')
