from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal User'),
        ('blood_bank', 'Blood Bank'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username

class BloodBank(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='blood_bank')
    organization_name = models.CharField(max_length=255)

    def __str__(self):
        return self.organization_name

class NormalUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='normal_user')
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username



class Donation(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donations')
    # The blood bank (donation center) is selected from registered blood banks.
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='donation_requests')
    # The donated amount (units, liters, etc.)
    donated_amount = models.DecimalField(max_digits=5, decimal_places=2)
    # Date and time when the donor wishes to donate.
    scheduled_datetime = models.DateTimeField()
    # Auto-populated timestamp when the donation request is created.
    request_datetime = models.DateTimeField(auto_now_add=True)
    # Confirmation status set by the blood bank.
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation by {self.donor.username} on {self.scheduled_datetime:%Y-%m-%d %H:%M}"