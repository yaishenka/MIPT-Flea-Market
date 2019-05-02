from django.shortcuts import render, redirect, HttpResponse
from .tasks import send_vk_message
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def vk_callback(request):
    request_type = json.loads(request.body.decode('utf-8')['type']
    if request_type == "confirmation":
        return HttpResponse("07ca78fc", content_type="text/plain", status=200)
    return redirect('ads_list')
