from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from mountains.views import home

urlpatterns = [path("admin/", admin.site.urls), path("i18n/", include("django.conf.urls.i18n")), path("", home, name="home"), path("accounts/", include("accounts.urls")), path("mountains/", include("mountains.urls")), path("hikes/", include("hikes.urls")), path("stories/", include("community.urls")), path("weather/", include("weather.urls")), path("assistant/", include("ai_assistant.urls"))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
