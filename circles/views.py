from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    DeleteView,
    FormView,
)
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.core.mail import send_mail

from .models import Event
from .forms import EventHostForm, JoinForm


User = get_user_model()


class EventList(ListView):
    """Listing of upcoming events"""

    context_object_name = "events"
    queryset = Event.objects.upcoming().prefetch_related("participants")


class EventHost(CreateView):
    """Create/Host a new event"""

    model = Event
    form_class = EventHostForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user, _ = User.objects.get_or_create(email=email, username=email)
        event = form.instance
        event.host = user
        event.save()

        send_mail(
            "Event erstellt",
            f"Dein Event um {event.start} wurde erstellt. Wir schicken dir einen Link, wenn es anfängt.",
            "from@example.com",
            [email],
        )

        return render(self.request, "circles/hosted.html", {"event": event})


class EventDeleteView(DeleteView):
    """Allows the host to delete the event. Secret Link"""

    # TODO: This is only an idea
    model = Event


class EventJoin(FormView):
    """Allows to join the event
    
    Asks user for mail. Sends mail with details for event"""

    template_name = "circles/join_form.html"
    form_class = JoinForm

    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs["id"])
        data = super().get_context_data(**kwargs)
        data["event"] = event
        return data

    def form_valid(self, form):
        event = Event.objects.get(pk=self.kwargs["id"])

        if event.is_full or event.is_past:
            return render(
                self.request, "circles/full_or_past.html", {"event": event}, status=400
            )

        email = form.cleaned_data["email"]
        user, _ = User.objects.get_or_create(email=email, username=email)

        if user not in event.participants.all():
            event.participants.add(user)

        send_mail(
            "Event beigetreten",
            f"Du bist einem Event um {event.start} beigetreten. Wir schicken dir einen Link, wenn es anfängt.",
            "from@example.com",
            [email],
        )

        return render(self.request, "circles/joined.html", {"event": event})
