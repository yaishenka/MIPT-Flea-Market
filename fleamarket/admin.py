"""Registration models for django admin"""

from django.contrib import admin
from .models import AbstractAd


admin.site.register(AbstractAd)
