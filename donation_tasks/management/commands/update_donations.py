from django.core.management.base import BaseCommand
from main.models import Donation

class Command(BaseCommand):
    help = 'Update the status of all Donation objects'

    def handle(self, *args, **kwargs):
        donations = Donation.objects.all()
        for donation in donations:
            donation.update_status()
        self.stdout.write(self.style.SUCCESS('Successfully updated donation statuses.'))
