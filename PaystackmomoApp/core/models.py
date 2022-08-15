from codecs import charmap_build
import email
from locale import currency
import secrets
from django.db import models
from .paystack import Paystack

# Create your models here.

class MobileMoneyProfile(models.Model):
    owner = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    provider = models.CharField(max_length = 5)
    number = models.CharField(max_length = 50)
    currency = models.CharField(max_length = 150)
        
    
class BankPaymentProfile(models.Model):
    owner = models.ForeignKey('auth.user', on_delete=models.CASCADE,related_name='bankowners')
    name = models.CharField(max_length = 150)
    bank_name = models.CharField(max_length = 150)
    account_name = models.CharField(max_length = 150)
    account_number = models.CharField(max_length = 150)

class MomoPayment(models.Model):
    owner = models.ForeignKey(MobileMoneyProfile, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    ref = models.CharField(max_length=200)
    amount = models.PositiveBigIntegerField()
    verified = models.BooleanField(default=False)
    currency_charged = models.CharField(max_length=3)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return f'Payment: {self.amount}'

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            same_ref = MomoPayment.objects.filter(ref=ref)
            if not same_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()

        if self.verified:
            return True

        return False


class BankPayment(models.Model):
    owner = models.ForeignKey(BankPaymentProfile, on_delete=models.CASCADE)
    ref = models.CharField(max_length=200)
    amount = models.PositiveBigIntegerField()
    verified = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return f'Payment: {self.amount}'

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            same_ref = BankPayment.objects.filter(ref=ref)
            if not same_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()

        if self.verified:
            return True

        return False
     

  
  
  