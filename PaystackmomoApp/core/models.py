import email
from locale import currency
import secrets
from django.db import models
from .paystack import Paystack

# Create your models here.


class Payment(models.Model):
    email = models.EmailField(max_length=200)
    ref = models.CharField(max_length=200)
    amount = models.PositiveBigIntegerField()
    verified = models.BooleanField(default=False)
    currency_charged = models.CharField(max_length=3)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return f'Payment: {self.name}'

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            same_ref = Payment.objects.filter(ref=ref)
            if not same_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def anount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack_verify_payment(self.ref, self.amount)
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
