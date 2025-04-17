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
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    loc_latitude = models.DecimalField(max_digits=10, decimal_places=7, default=19.1674517)
    loc_longitude = models.DecimalField(max_digits=10, decimal_places=7, default=72.8513831)
    email = models.EmailField(unique=False, blank=True, null=True)

    def __str__(self):
        return self.username

class BloodBank(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='blood_bank')
    organization_name = models.CharField(max_length=255)
    website = models.URLField(default='https://example.com')
    max_capacity_per_group = models.PositiveIntegerField(default=100)  # Set default max capacity per group.
    a0=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    a1=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    b0=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    b1=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ab0=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ab1=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    o0=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    o1=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def calculate_stock_percentage(self,blood_group):
        if blood_group == 'A+':
            return round((self.a1 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'A-':
            return round((self.a0 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'B+':
            return round((self.b1 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'B-':
            return round((self.b0 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'AB+':
            return round((self.ab1 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'AB-':
            return round((self.ab0 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'O+':
            return round((self.o1 / self.max_capacity_per_group) * 100, 2)
        elif blood_group == 'O-':
            return round((self.o0 / self.max_capacity_per_group) * 100, 2)
        else:
            return 0.00


    def __str__(self):
        return self.organization_name

    
class NormalUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='normal_user')
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username

from django.utils.timezone import now

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
    # confirmed = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('not_confirmed', 'Not Confirmed'),
        ('pending', 'Confirmed but Pending'),
        ('donated', 'Donated'),
        ('not_accepted', 'Not Accepted')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_confirmed')
    not_accepted_reason = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Donation by {self.donor.username} on {self.scheduled_datetime:%Y-%m-%d %H:%M}"
    
    def update_status(self):
        current_time = now()
        if self.status == 'pending' and self.scheduled_datetime < current_time:
            self.status = 'donated'
        elif self.status == 'not_confirmed' and self.scheduled_datetime < current_time:
            self.status = 'not_accepted'
            self.not_accepted_reason = "The scheduled time has passed without confirmation."
        self.save()
    
class DonationRequest(models.Model):
    blood_bank= models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='request_donation')
    blood_group = models.CharField(max_length=5)
    requested_amount = models.DecimalField(max_digits=5, decimal_places=2)
    request_datetime = models.DateTimeField( null=False, blank=False)
    sent_requests=models.DecimalField(max_digits=10,default=0,decimal_places=0)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('not_fulfilled', 'Not Fulfilled')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    additional_info = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"Donation request by {self.blood_bank.organization_name} for {self.blood_group} on {self.request_datetime:%Y-%m-%d %H:%M}"
    
class FulfilledRequests(models.Model):
    # donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='fulfilled_requests')
    donation_req_id = models.DecimalField(max_digits=10, decimal_places=0,null=False, blank=False)
    fulfilled_by = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='fulfilled_donations',blank=True,null=True)
    user_ids = models.ManyToManyField(NormalUser, related_name='participated_fulfillments', blank=True)

    def __str__(self):
        return f"Fulfilled request {self.donation_req_id}"