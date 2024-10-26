import requests
from django.conf import settings

def get_paypal_access_token():
    url = f"{settings.PAYPAL_API_URL}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {
        "grant_type": "client_credentials",
    }
    
    response = requests.post(url, headers=headers, data=data, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET))
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception('Failed to obtain PayPalaccesstoken.')
    

def get_paypal_payment_details(payment_id):
    access_token = get_paypal_access_token()
    
    url = f"{settings.PAYPAL_API_URL}/v2/checkout/orders/{payment_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch PayPal payment details. Status code: {response.status_code}, Response: {response.json()}")