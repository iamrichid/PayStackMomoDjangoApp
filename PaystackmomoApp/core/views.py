from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets,permissions
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly

from .forms import PaymentForms
from .models import BankPaymentProfile, MobileMoneyProfile
from .serializers import (BankProfileSerializer, MobileMoneyProfileSerializer,
                         PaymentVerificationSerializer,
                          UserSerializer)

# Create your views here.



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MoMoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset = MobileMoneyProfile.objects.all()
    serializer_class = MobileMoneyProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the Profile
        for the currently authenticated user.
        """
        user = self.request.user.id
        return MobileMoneyProfile.objects.filter(owner_id=user)

class BankViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset = BankPaymentProfile.objects.all()
    serializer_class = BankProfileSerializer
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the Profile
        for the currently authenticated user.
        """
        user = self.request.user.id
        print(f'{user} the id of the user')
        return BankPaymentProfile.objects.filter(owner_id=user) 

    

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
    # payment = get_object_or_404(Payment, ref=ref)
    # verified = payment.verify_payment()

    if verified:
        messages.success(request, "verification successful")
    else:
        messages.error(request, 'verification failed')
    return redirect('initiate payment')
