from django.urls import path
from . import views

app_name = "circles"

urlpatterns = [
    path("", views.EventList.as_view(), name="list"),
    path("host", views.EventHost.as_view(), name="host"),
    path("participate/<int:id>", views.EventJoin.as_view(), name="participate"),
    path("leave/<uuid:uuid>", views.EventLeaveView.as_view(), name="leave",),
    path("delete/<uuid:uuid>", views.EventDeleteView.as_view(), name="delete"),
]
