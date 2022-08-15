
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (BankPaymentProfile, MobileMoneyProfile, MomoPayment,
                    )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class PaymentVerificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= MomoPayment
        fields = ('email', 'amount', 'ref')

class MobileMoneyProfileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = MobileMoneyProfile
        fields = ('__all__')   
         
        

class BankProfileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = BankPaymentProfile
        fields = ('__all__')    
