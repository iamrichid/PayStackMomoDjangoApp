from django.test import TestCase
from rest_framework.test import APITestCase

from core.paystack import MakePaymentWithPayStack

# Create your tests here.

class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)



make_payment_with_paystack = MakePaymentWithPayStack()


class PaymentOptionWithPaystack(APITestCase):
    def test_charge_with_momo(self):
        payload = {
            "email": "customer@gmail.com",
            "amount": 100000,
            "mobile_money": {"phone": "0551234987", "provider": "MTN"},
            "currency": "GHS",
        }
        response = make_payment_with_paystack.charge_with_mobile_money(payload)
        self.assertEqual(response["status"], True)
        self.assertEqual(response["message"], "Charge attempted")
        self.assertEqual(response["data"]["channel"], "mobile_money")
        self.assertEqual(response["data"]["currency"], "GHS")
        self.assertEqual(response["data"]["amount"], 100000)

    def test_bank_transfer(self):
        payload ={ 
            "email": "customer@email.com", 
            "amount": "10000", 
            "bank": {
                      "code": "057", 
                      "account_number": "0000000000" 
                   },
                
        }

        response = make_payment_with_paystack.charge_with_bank(payload)
        print(f'{response}')
        self.assertEqual(response["status"], True)
        self.assertEqual(response["message"], "1 transfers queued.")
        data = response["data"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["recipient"], payload["transfers"][0]["recipient"])
        self.assertEqual(data[0]["amount"], payload["transfers"][0]["amount"])

       