from django.shortcuts import render, redirect, HttpResponse
from .tasks import send_vk_message, send_vk_message_by_uid
from django.views.decorators.csrf import csrf_exempt
from fleamarket.models import AbstractAd
import json


# Create your views here.
@csrf_exempt
def vk_callback(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        request_type = data['type']
    except:
        return HttpResponse("ok", content_type="text/plain", status=200)
    if request_type == "confirmation":
        return HttpResponse("07ca78fc", content_type="text/plain", status=200)
    elif request_type == "message_new":
        vk_parse_message(data['object'])
    return HttpResponse("ok", content_type="text/plain", status=200)



@csrf_exempt
def vk_help(user_id):
    send_vk_message_by_uid(user_id,
                           'Привет) Я бот "Барахолки Физтеха". Напиши мне "объявления", чтобы получить список всех объявлений. Напиши category_name(список ниже), чтобы получить объявления определенной категории. Достыпные категории: {}'.format(
                               [category[0] for category in
                                AbstractAd.CATEGORIES]))


@csrf_exempt
def vk_error(user_id):
    send_vk_message_by_uid(user_id,
                           'Я не знаю такой команды( Напиши "помощь", если хочешь увидеть доступные команды')


@csrf_exempt
def send_ad_in_category(user_id, category):
    message_text = ''
    for ad in AbstractAd.objects.filter(category=category):
        ad_text = '''Автор - {0} \n
                         {1} \n
                         {2} \n
                      '''.format(ad.seller.get_full_name, ad.header, ad.text)
        ad_text += 'Ссылка - yaishenka.site/ad/{}'.format(ad.pk)
        message_text += ad_text + '\n'

    send_vk_message_by_uid(user_id,
                           'Доступные объявления: {}'.format(message_text))


@csrf_exempt
def send_all_ads(user_id):
    message_text = ''
    for ad in AbstractAd.objects.all():
        ad_text = '''Автор - {0} \n
                     {1} \n
                     {2} \n
                  '''.format(ad.seller.get_full_name, ad.header, ad.text)
        ad_text += 'Ссылка - yaishenka.site/ad/{}'.format(ad.pk)
        message_text += ad_text + '\n'

    send_vk_message_by_uid(user_id,
                           'Доступные объявления: {}'.format(message_text))


@csrf_exempt
def vk_parse_message(message_object):
    message_text = message_object['text']
    from_user = message_object['from_id']

    if message_text.lower() == 'помощь':
        vk_help(from_user)
    elif message_text.lower() == 'объявления':
        send_all_ads(from_user)
    elif message_text.lower() in [category[0] for category in
                                  AbstractAd.CATEGORIES]:
        send_ad_in_category(from_user, message_text.lower())
    else:
        vk_error(from_user)
