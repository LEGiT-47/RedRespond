from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('normal-home/', views.normal_home, name='normal_home'),
    path('blood-bank-home/', views.blood_bank_home, name='blood_bank_home'),
    path('logout/', views.logout_view, name='logout'),
    # path('donate/', views.donation_request_view, name='donation_request'),
    path('donate/success/', views.donation_request_success_view, name='donation_request_success'),
    path('bloodbank/requests/', views.donation_requests_view, name='donation_requests'),
    path('donations/past/', views.past_donations_view, name='past_donations'),
    path('bd_page/<int:id>/', views.blood_donation_page, name='blood_donation_page'),
    path('donation/details/<int:id>/', views.donation_detail, name='donation_detail'),
    # path('', views.send_request_form, name='send_request'),
    path('request-blood-phone/<str:phone_number>/', views.request_blood_by_phone, name='request_blood_by_phone'),
    path('webhook-info/', views.webhook_info, name='webhook_info'),
    path('webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('donation-request-summary/<int:request_id>/', views.donation_request_summary, name='donation_request_summary'),
]
