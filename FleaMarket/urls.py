from .views import ads_list, create_ad
from django.urls import path

urlpatterns = [
    path('', ads_list, name='ads_list'),
    path('ad/new/', create_ad, name='new_ad')
]