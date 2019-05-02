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
                  path('', include('fleamarket.urls')),
                  path('', include('users.urls')),
                  path('user/', include('users.urls')),
                  path('vk_callback/', include('vk_sender.urls')),
                  path('subs/', include('subscriptions.urls')),
                  path('social/', include('social_django.urls', namespace='social'))
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
