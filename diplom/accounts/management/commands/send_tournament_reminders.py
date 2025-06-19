from django.core.management.base import BaseCommand
from django.utils import timezone
from ...signals import check_tournament_start

class Command(BaseCommand):
    help = 'Sends reminders for upcoming tournaments'

    def handle(self, *args, **options):
        self.stdout.write('Checking for upcoming tournaments...')
        check_tournament_start()
        self.stdout.write('Reminder check completed')