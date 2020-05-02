from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns += i18n_patterns(
    [
        path("admin/", admin.site.urls),
        path(_("circles/"), include("circles.urls")),
        path("", include("homepage.urls")),
        path("/", include("django.contrib.flatpages.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
