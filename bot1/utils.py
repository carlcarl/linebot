import hmac
import hashlib
import base64

import requests


def legal_signature(request_signature, msg, secret):
    dig = hmac.new(secret.encode('utf-8'), msg, digestmod=hashlib.sha256).digest()
    computed_signature = base64.b64encode(dig).decode()
    return computed_signature == request_signature


def create_msg_headers(channel_id, channel_secret, channel_mid):
    headers = {
        'X-Line-ChannelID': channel_id,
        'X-Line-ChannelSecret': channel_secret,
        'X-Line-Trusted-User-With-ACL': channel_mid,
    }
    return headers


def send_msg(headers, target_mids, content='', to_channel='1383378250', event_type='138311608800106203'):
    json_data = {
        'to': target_mids,
        'toChannel': to_channel,
        'eventType': event_type,
        'content': {
            'contentType': 1,
            'toType': 1,
            'text': content,
        },
    }
    response = requests.post('https://trialbot-api.line.me', json=json_data, headers=headers)
    return response
