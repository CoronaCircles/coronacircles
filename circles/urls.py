from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "circles"

urlpatterns = [
    path("", views.EventList.as_view(), name="list"),
    path(_("host"), views.EventHost.as_view(), name="host"),
    path(_("participate/<int:id>"), views.EventJoin.as_view(), name="participate"),
]
