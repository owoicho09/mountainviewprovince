import requests
import hashlib
import json
from django.conf import settings
import uuid
class RemitaPayment:
    def __init__(self, order_id, amount, payer_name, payer_email, payer_phone):
        self.order_id = order_id
        self.amount = str(int(float(amount)))
        self.payer_name = payer_name
        self.payer_email = payer_email
        self.payer_phone = payer_phone

    def generate_hash(self):
        """
        Generate the hash required for remita transaction
        """
        hash_string = f"{settings.REMITA_MERCHANT_ID}{self.order_id}{self.amount}{settings.REMITA_API_KEY}"
        print('hash_string----', hash_string)
        return hashlib.sha512(hash_string.encode()).hexdigest()

    def initialize_payment(self):
        """
        Initialize payment and get the RRR (Remita Retrieval Reference)
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'remitaConsumerKey={settings.REMITA_MERCHANT_ID},remitaConsumerToken={self.generate_hash()}'
        }
        print('headers-------', headers)

        payload = {
            "serviceTypeId": settings.REMITA_SERVICE_TYPE_ID,
            "amount": str(int(float(self.amount))),
            "orderId": str(self.order_id),
            "payerName": str(self.payer_name),
            "payerEmail": str(self.payer_email),
            "payerPhone": f'234{self.payer_phone}',
            "description": "Hostel payment"
        }

        print('Payload:', payload)

        url = f"{settings.REMITA_BASE_URL}/generateRRR"

        print('url---------', url)
        print('Payload:', json.dumps(payload))

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print('respomse--------', response)

        print("Response status code:", response.status_code)
        print("Response headers:", response.headers)
        print("Response content:", response.content)

        if response.status_code == 200:
            data = response.json()
            print('Response Data:', data)
            if data['statuscode'] == '00':
                return data['RRR']
            else:
                print(f"Error from Remita: {data['status']}")
        else:
            print(f"Failed to reach Remita API. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

    def check_payment_status(self, rrr):
        """
        Check the status of a payment using RRR.
        """
        hash_string = f"{settings.REMITA_MERCHANT_ID}{rrr}{settings.REMITA_API_KEY}"
        hash_value = hashlib.sha512(hash_string.encode()).hexdigest()

        url = f"{settings.REMITA_BASE_URL}/{settings.REMITA_MERCHANT_ID}/{rrr}/{hash_value}/status.reg"
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
