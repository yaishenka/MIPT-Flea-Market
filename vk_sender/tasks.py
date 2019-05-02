import requests
from django.conf import settings
from django.contrib.auth import get_user_model
import json

def send_vk_api_request(method_name, token, data):
    data['v'] = settings.VK_API_VERSION
    data['access_token'] = token
    response = requests.get('https://api.vk.com/method/{}'.format(method_name), params=data)
    return response.json()

def send_vk_message_by_uid(uid, message):
    data = {}
    data['user_id'] = uid
    data['message'] = message
    send_vk_api_request('messages.send', token=settings.VK_API_KEY, data=data)

def send_vk_message(user_id, message, *args, **kwargs):
    user = get_user_model().objects.get(id=user_id)
    for auth in user.social_auth.all():
        uid = auth.uid
        send_vk_message_by_uid(uid, message)


def send_vk_message_with_photos(user_id, message, photo):
    user = get_user_model().objects.get(id=user_id)
    for auth in user.social_auth.all():
        uid = auth.uid
        data = {}
        photo = upload_photo(uid, settings.VK_API_KEY, photo.path)
        data['attachment'] = photo
        data['user_id'] = uid
        data['message'] = message
        send_vk_api_request('messages.send', token=settings.VK_API_KEY, data=data)


def upload_photo(uid, token, photo_path):
    res = send_vk_api_request('photos.getMessagesUploadServer', token, {'peer_id': uid})
    if 'response' in res:
        upload_url = res['response']['upload_url']
        photo_file = open(photo_path, "rb")
        response = requests.post(upload_url, files={'photo': photo_file})
        params = {'server': response.json()['server'],
                  'photo': response.json()['photo'],
                  'hash': response.json()['hash']}
        res = send_vk_api_request('photos.saveMessagesPhoto', token, params)
        print(photo_file)
        print(photo_path)
        print(res)
        photo_file.close()
        if 'response' in res:
            data = res['response'][0]
            owner_id = data['owner_id']
            media_id = data['id']
            photo_send = 'photo{0}_{1}'.format(owner_id, media_id)
            return photo_send
