"""
Root URL configuration for the AI Telephony Assistant.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # Properties REST API
    path("api/", include("apps.properties.urls")),

    # Twilio webhook endpoints
    path("", include("apps.telephony.urls")),
]
