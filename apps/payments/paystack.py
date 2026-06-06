"""
SIBRAH Payments — Paystack Service
apps/payments/paystack.py

All Paystack API communication goes through this file.
"""

import uuid
import hmac
import hashlib
import json
import urllib.request
import urllib.parse
import urllib.error
from django.conf import settings


PAYSTACK_BASE = 'https://api.paystack.co'


def _get_secret_key():
    """Return the Paystack secret key from settings."""
    return getattr(settings, 'PAYSTACK_SECRET_KEY', '')


def _headers():
    return {
        'Authorization': f'Bearer {_get_secret_key()}',
        'Content-Type':  'application/json',
    }


def _post(endpoint, data):
    """Make a POST request to Paystack API."""
    url     = f"{PAYSTACK_BASE}{endpoint}"
    payload = json.dumps(data).encode('utf-8')
    req     = urllib.request.Request(url, data=payload, headers=_headers(), method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return json.loads(body)
        except Exception:
            return {'status': False, 'message': str(e)}
    except Exception as e:
        return {'status': False, 'message': str(e)}


def _get(endpoint):
    """Make a GET request to Paystack API."""
    url = f"{PAYSTACK_BASE}{endpoint}"
    req = urllib.request.Request(url, headers=_headers(), method='GET')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return json.loads(body)
        except Exception:
            return {'status': False, 'message': str(e)}
    except Exception as e:
        return {'status': False, 'message': str(e)}


def generate_reference(prefix='SIBRAH'):
    """Generate a unique payment reference."""
    unique = str(uuid.uuid4()).replace('-', '')[:12].upper()
    return f"{prefix}-{unique}"


def initialize_transaction(email, amount_naira, reference, callback_url,
                            metadata=None, channels=None):
    """
    Initialize a Paystack transaction.

    Args:
        email        : Customer email
        amount_naira : Amount in Nigerian Naira (we convert to kobo)
        reference    : Unique transaction reference
        callback_url : URL Paystack redirects to after payment
        metadata     : dict of extra data stored with the transaction
        channels     : list e.g. ['card', 'bank', 'ussd', 'bank_transfer']

    Returns:
        dict with keys: status, authorization_url, access_code, reference
    """
    amount_kobo = int(amount_naira * 100)   # Paystack works in kobo

    data = {
        'email':        email,
        'amount':       amount_kobo,
        'reference':    reference,
        'callback_url': callback_url,
        'currency':     'NGN',
        'metadata':     metadata or {},
    }

    if channels:
        data['channels'] = channels

    response = _post('/transaction/initialize', data)

    if response.get('status'):
        return {
            'status':            True,
            'authorization_url': response['data']['authorization_url'],
            'access_code':       response['data']['access_code'],
            'reference':         response['data']['reference'],
            'amount_kobo':       amount_kobo,
        }
    return {
        'status':  False,
        'message': response.get('message', 'Failed to initialize transaction'),
    }


def verify_transaction(reference):
    """
    Verify a Paystack transaction by reference.

    Returns:
        dict with status, amount (naira), channel, paid_at, gateway_response, etc.
    """
    response = _get(f'/transaction/verify/{reference}')

    if response.get('status') and response.get('data'):
        data = response['data']
        return {
            'status':           True,
            'transaction_status': data.get('status'),           # 'success', 'failed', etc.
            'amount_naira':     data.get('amount', 0) / 100,    # convert kobo → naira
            'amount_kobo':      data.get('amount', 0),
            'channel':          data.get('channel', ''),
            'currency':         data.get('currency', 'NGN'),
            'reference':        data.get('reference', reference),
            'paystack_id':      str(data.get('id', '')),
            'gateway_response': data.get('gateway_response', ''),
            'paid_at':          data.get('paid_at'),
            'customer_email':   data.get('customer', {}).get('email', ''),
            'customer_name':    data.get('customer', {}).get('first_name', ''),
            'metadata':         data.get('metadata', {}),
        }

    return {
        'status':  False,
        'message': response.get('message', 'Verification failed'),
    }


def verify_webhook_signature(payload_bytes, paystack_signature):
    """
    Verify that a webhook came from Paystack.
    Uses HMAC-SHA512 with your secret key.
    """
    secret = _get_secret_key().encode('utf-8')
    computed = hmac.new(secret, payload_bytes, hashlib.sha512).hexdigest()
    return hmac.compare_digest(computed, paystack_signature)
