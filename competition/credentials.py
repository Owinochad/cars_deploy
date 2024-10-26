import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from decouple import config
from django.conf import settings



class MpesaC2bCredential:
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    token_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


class MpesaAccessToken:
    @staticmethod
    def get_access_token():
        r = requests.get(MpesaC2bCredential.token_url,
                         auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
        if r.status_code == 200:
            mpesa_access_token = json.loads(r.text)
            return mpesa_access_token.get("access_token")
        else:
            print("Failed to retrieve access token. Status Code:", r.status_code)
            print("Response:", r.text)
            return None


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = settings.BUSINESS_SHORT_CODE
    passkey = settings.PASSKEY

    data_to_encode = business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
