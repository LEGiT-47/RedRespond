from django.contrib import admin
from .models import CustomUser, BloodBank, NormalUser, Donation, DonationRequest, FulfilledRequests 

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'city', 'state')
    list_filter = ('user_type',)

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user', 'max_capacity_per_group', 'a0', 'a1', 'b0', 'b1', 'ab0', 'ab1', 'o0', 'o1')

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

@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('blood_bank', 'blood_group', 'requested_amount', 'request_datetime', 'status')
    list_filter = ('status', 'blood_group')
    search_fields = ('blood_bank__username', 'blood_group')

@admin.register(FulfilledRequests)
class FulfilledRequestsAdmin(admin.ModelAdmin):
    list_display = ('donation_req_id', 'fulfilled_by', 'get_user_ids')
    list_filter = ('donation_req_id', 'fulfilled_by')
    search_fields = ('donation_req_id', 'fulfilled_by__user__username')

    def get_user_ids(self, obj):
        return ", ".join([str(user) for user in obj.user_ids.all()])
    get_user_ids.short_description = 'Participating Users'

