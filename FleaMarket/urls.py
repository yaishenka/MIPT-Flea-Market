from .views import ads_list, create_ad, change_ad, view_ad, delete_ad
from django.urls import path

urlpatterns = [
    path('', ads_list, name='ads_list'),
    path('ad/new/', create_ad, name='new_ad'),
    path('ad/<int:pk>/change', change_ad, name='change_ad'),
    path('ad/<int:pk>/', view_ad, name='view_ad'),
    path('ad/delete/<int:pk>/', delete_ad, name='delete_ad')
]