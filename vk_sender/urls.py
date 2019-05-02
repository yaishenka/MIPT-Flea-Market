from django.urls import path, include
from .views import vk_callback


urlpatterns = [
    path('', vk_callback, name='vk_callback')
]