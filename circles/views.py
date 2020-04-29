from django.views.generic import ListView, CreateView, TemplateView, DeleteView
from django.urls import reverse

from .models import Event
from .forms import EventHostForm


class EventList(ListView):
    model = Event


class EventHost(CreateView):
    model = Event
    form_class = EventHostForm
    success_url = "/success"  # TODO: Use reverse

    # TODO: Create User from email field


class EventHostSuccess(TemplateView):
    template_name = "circles/success.html"


class EventDeleteView(DeleteView):
    """Allows the host to delete the event. Secret Link"""

    # TODO: This is only an idea
    model = Event
