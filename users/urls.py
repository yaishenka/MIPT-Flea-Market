from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('<int:user_id>', views.user_view, name='user_view'),
    path('private_office', views.private_office, name='private_office')
    #TODO ChangePassword, ForgotPassword
]