from django.conf import settings
from django.http import HttpResponse
import requests


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f' /transaction/verify/{ref}'

        headers = {
            'Authorization': f' bearer{PAYSTACK_SECRET_KEY} ',
            'Content-Type': 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        return response_data['status'], response_data['message']