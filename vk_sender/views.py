from django.shortcuts import render, redirect
from .tasks import send_vk_message

# Create your views here.

def test_vk(request):
    send_vk_message(27894099 )
    return redirect('ads_list')
