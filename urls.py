from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("circles/", include("circles.urls")),
    path("", include("homepage.urls")),
    path("/", include("django.contrib.flatpages.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
