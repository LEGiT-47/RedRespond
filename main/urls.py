from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('normal-home/', views.normal_home, name='normal_home'),
    path('blood-bank-home/', views.blood_bank_home, name='blood_bank_home'),
    path('logout/', views.logout_view, name='logout'),
    path('donate/', views.donation_request_view, name='donation_request'),
    path('donate/success/', views.donation_request_success_view, name='donation_request_success'),
    path('bloodbank/requests/', views.donation_requests_view, name='donation_requests'),
    path('donations/past/', views.past_donations_view, name='past_donations'),
]
