from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon_view)
]
