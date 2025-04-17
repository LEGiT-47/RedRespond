from celery import shared_task
from .models import Donation

@shared_task
def update_donations():
    print("Updating donation statuses...")
    donations = Donation.objects.all()
    for donation in donations:
        print(f"Processing donation: {donation}")
        try:
            donation.update_status()
            print(f"Updated donation status for {donation.donor.username} on {donation.scheduled_datetime:%Y-%m-%d %H:%M}")
        except Exception as e:
            print(f"Error processing donation {donation}: {e}")

