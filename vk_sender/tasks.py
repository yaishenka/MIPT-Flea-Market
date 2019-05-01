import requests
from django.conf import settings
import json

def send_vk_api_request(method_name, token, data):
    data['v'] = settings.VK_API_VERSION
    data['access_token'] = token
    response = requests.get('https://api.vk.com/method/{}'.format(method_name), params=data)

def send_vk_message(user_id, message, *args, **kwargs):
    data = {}
    data['user_id'] = user_id
    data['message'] = message
    send_vk_api_request('messages.send', token=settings.VK_API_KEY, data=data)

def send_vk_message_with_photos(user_id, message, photo):
    pass
