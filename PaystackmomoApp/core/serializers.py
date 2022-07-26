from .models import Payment
from rest_framework import serializers
from django.contrib.auth.models import User



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Payment
        fields = ('email', 'amount')   

class PaymentVerificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Payment
        fields = ('email', 'amount', 'ref')