from django.urls import path
from . import views

urlpatterns = [
    path('control_subs', views.control_subscriptions, name='control_subs'),
    path('subscribe/<int:subscription_id>', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:subscription_id>', views.unsubscribe, name='unsubscribe')
]