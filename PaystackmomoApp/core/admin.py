from django.contrib import admin
from .models import BankPaymentProfile, MobileMoneyProfile

# Register your models here.

admin.site.register(MobileMoneyProfile)
admin.site.register(BankPaymentProfile)
