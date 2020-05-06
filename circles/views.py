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
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import Event, MailTemplate
from .forms import Host, Participate


User = get_user_model()


class EventList(ListView):
    """Listing of upcoming events"""

    context_object_name = "events"
    template_name = "circles/list.html"
    queryset = Event.objects.upcoming().prefetch_related("participants")


class EventHost(CreateView):
    """Create/Host a new event"""

    model = Event
    template_name = "circles/host.html"
    form_class = Host

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user, _ = User.objects.get_or_create(email=email, username=email)
        event = form.instance
        event.host = user
        event.save()

        # send mail
        mail = MailTemplate.get_mail(
            type="host_confirmation", context={"event": event}, to_email=email,
        )
        if mail:
            mail.attach(
                filename="event.ical", content=event.ical, mimetype="text/calendar"
            )
            mail.send(fail_silently=True)

        return render(self.request, "circles/hosted.html", {"event": event})


class EventDeleteView(DeleteView):
    """Allows the host to delete the event."""

    model = Event
    success_url = "/"
    context_object_name = "event"

    def get_object(self):
        return Event.objects.get(uuid=self.kwargs["uuid"])

    def delete(self, request, *args, **kwargs):
        # mail participants
        event = self.get_object()
        event.mail_participants(template_type="deleted")

        return super().delete(request, *args, **kwargs)


class EventJoin(FormView):
    """Allows to join the event
    
    Asks user for mail. Sends mail with details for event"""

    template_name = "circles/participate.html"
    form_class = Participate

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

        # send mail
        mail = MailTemplate.get_mail(
            type="join_confirmation", context={"event": event}, to_email=email,
        )
        if mail:
            mail.attach(
                filename="event.ical", content=event.ical, mimetype="text/calendar"
            )
            mail.send(fail_silently=True)

        return render(self.request, "circles/participated.html", {"event": event})
