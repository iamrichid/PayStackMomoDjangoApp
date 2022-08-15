from asyncio.log import logger
import json
from django.conf import settings
from django.http import HttpResponse
import requests


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f'/transaction/verify/{ref}'

        headers = {
            'Authorization': f'Bearer {self.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']


class MakePaymentWithPayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co/'

    def _send_request(self, data: dict, endpoint: str):
        try:
            url = self.base_url + endpoint
            headers = {
                'Authorization': f'Bearer {self.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            }

            response = requests.post(url, data=json.dumps(data), headers=headers)

            return json.loads(response.text)
        except Exception as error:
            logger.error(str(error))

    def _charge(self, data: dict):
        return self._send_request(data=data, endpoint="charge")

    def charge_with_mobile_money(self, data: dict):
        return self._charge(data)

    def charge_with_card(self, data: dict):
        return self._charge(data)

    def charge_with_bank(self, data: dict):
        return self._charge(data)    

    def create_transfer_recipient(self, user_details: dict):
        return self._send_request(data=user_details, endpoint="transferrecipient")

    def bank_transfer(self, data: dict):
        return self._send_request(data=data, endpoint="transfer/bulk")