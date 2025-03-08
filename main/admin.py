from django.contrib import admin
from .models import CustomUser, BloodBank, NormalUser, Donation

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'city', 'state')
    list_filter = ('user_type',)

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user')

@admin.register(NormalUser)
class NormalUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'donor', 
        'blood_bank', 
        'donated_amount', 
        'scheduled_datetime', 
        'request_datetime', 
        'status',
    )
    list_filter = ('status', 'blood_bank')
    search_fields = ('donor__username', 'blood_bank__organization_name')

