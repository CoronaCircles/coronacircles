from django.core.management.base import BaseCommand

from circles.models import Event


class Command(BaseCommand):
    help = "Mail the participants of events that are about to start (best run via cron every 5 minutes)"

    def mail_participants(self):
        for event in Event.objects.to_be_mailed():
            event.mail_participants()

    def delete_old_events(self):
        for event in Event.objects.to_be_deleted():
            event.delete()

    def handle(self, *args, **options):
        self.mail_participants()
        self.delete_old_events()
