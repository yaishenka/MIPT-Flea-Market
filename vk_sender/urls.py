from django.urls import path, include
from .views import test_vk


urlpatterns = [
    path('', test_vk)
]