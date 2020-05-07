from django.urls import path
from . import views

app_name = "homepage"

urlpatterns = [
    path("<path:url>", views.SimplePageView.as_view(), name="page"),
    path("", views.Homepage.as_view(), name="index"),
]
