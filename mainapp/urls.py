from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico',
                                    permanent=True)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('favicon.ico', favicon_view),
                  path('flea_market/', include('fleamarket.urls')),
                  path('flea_market/', include('users.urls')),
                  path('social/', include('social_django.urls', namespace='social'))
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
