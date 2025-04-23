
from .forms import CustomUserCreationForm
from .models import BloodBank, NormalUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from .models import Donation, DonationRequest, FulfilledRequests 
from .forms import DonationRequestForm, DonationConfirmationForm,DonationRequestCreationForm
from django.utils import timezone
# 7714927470:AAHT8RMlguaBjQgVLI5yZ5rNn4lsvQAm4ow
from django.http import JsonResponse
import requests
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(1)
        print(form.errors)
        if form.is_valid():
            print(2)
            user = form.save(commit=False)
            latitude = request.POST.get('latitude')
            print(latitude)
            longitude = request.POST.get('longitude')
            print(longitude)
            user.save()

            # Save additional fields
            if user.user_type == 'blood_bank':
                b1=BloodBank.objects.create(
                    user=user,
                    organization_name=form.cleaned_data['organization_name'],

                )
                b1.user.loc_latitude = latitude
                b1.user.loc_longitude = longitude
                b1.user.save()
                b1.save()
                login(request, user)
                return redirect('blood_bank_home')  # Redirect blood bank users to their home
            elif user.user_type == 'normal':
                b1=NormalUser.objects.create(
                    user=user,
                    blood_group=form.cleaned_data['blood_group'],

                )
                b1.user.loc_latitude = latitude
                b1.user.loc_longitude = longitude
                b1.user.save()
                b1.save()
                login(request, user)
                return redirect('normal_home')  # Redirect normal users to their home
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})



def home(request):
    return render(request, 'main/home.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'normal':
            return redirect('normal_home')
        elif request.user.user_type == 'blood_bank':
            return redirect('blood_bank_home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to respective home page based on user type
            if user.user_type == 'normal':
                return redirect('normal_home')
            elif user.user_type == 'blood_bank':
                return redirect('blood_bank_home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


@login_required
def normal_home(request):
    """View for a donor to create a donation request."""
    if request.user.is_authenticated:
        profile = get_object_or_404(NormalUser, user=request.user)  # replace with actual model
        if not profile.user.telegram_chat_id:
            return redirect('connect_telegram')
    blood_groupiee=NormalUser.objects.get(user=request.user)
    # past_donations = Donation.objects.filter(donor=request.user).exclude(status='not_confirmed',status='not_accepted')
    already = Donation.objects.filter(donor=request.user,  status='donated')
    notconfirm= Donation.objects.filter(donor=request.user,status='not_confirmed')
    pending= Donation.objects.filter(donor=request.user, scheduled_datetime__gt=timezone.now(),status='pending')
    latest_donation = Donation.objects.filter(donor=request.user, status__in=['donated', 'pending','not_confirmed']).order_by('-scheduled_datetime').first()
    eligible = "True" if not latest_donation or (timezone.now() - latest_donation.scheduled_datetime).days >= 90 else "False"
    eligible_time = 90 - (timezone.now() - latest_donation.scheduled_datetime).days if latest_donation else None
    if request.method == "POST":
        form = DonationRequestForm(request.POST)
        if form.is_valid() and eligible == "True":
            donation = form.save(commit=False)
            donation.donor = request.user  # Automatically set donor from logged-in user
            donation.save()
            return redirect('donation_request_success')
    else:
          form = DonationRequestForm()
    return render(request, 'main/normal_home.html', {'form': form,'blood_groupiee':blood_groupiee,'already':already,'notconfirm':notconfirm,'pending':pending,'eligible':eligible,'eligible_time':eligible_time})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def connect_telegram(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(NormalUser, user=request.user)  # replace with actual model
        if profile.user.telegram_chat_id:
            return redirect('normal_home')
    return render(request, 'main/connect_telegram.html')


@login_required
def donation_request_success_view(request):
    """A simple success page after a donation request is submitted."""
    return render(request, 'donations/donation_request_success.html')

@login_required
def donation_requests_view(request):
    """
    View for a blood bank to see donation requests addressed to them.
    Only pending requests (confirmed=False) are shown.
    """
    # Ensure the logged-in user is a blood bank.
    try:
        blood_bank = request.user.blood_bank
    except Exception:
        return redirect('home')  # or show an error if the user is not a blood bank

    donation_requests = Donation.objects.filter(blood_bank=blood_bank,status='not_confirmed')

    # For each donation, we can handle a confirmation form.
    if request.method == "POST":
        donation_id = request.POST.get('donation_id')
        donation = get_object_or_404(Donation, id=donation_id, blood_bank=blood_bank)
        form = DonationConfirmationForm(request.POST, instance=donation)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('donation_requests')
    else:
        form = DonationConfirmationForm()

    return render(request, 'donations/donation_requests.html', {
        'donation_requests': donation_requests,
        'form': form
    })

@login_required
def past_donations_view(request):
    """View for a donor to see all confirmed (past) donations."""
    past_donations = Donation.objects.filter(donor=request.user, status='donated')
    for hell in past_donations:
        hell.blood_group= get_object_or_404(NormalUser,user=request.user).blood_group
    return render(request, 'donations/past_donations.html', {'past_donations': past_donations})

@login_required
def blood_donation_page(request,id):
    donation = get_object_or_404(Donation, id=id)
    if donation.status == 'not_accepted':
        return render(request, 'main/blood_donation_page.html', {'donation': donation, 'not_accepted': True})
    return render(request, 'main/blood_donation_page.html', {'donation': donation})



@login_required
def blood_bank_home(request):
    """
    View for a blood bank to see donation requests addressed to them.
    Only pending requests (confirmed=False) are shown.
    """
    try:
        blood_bank = request.user.blood_bank
    except Exception:
        return redirect('home')  # Redirect if user is not a blood bank

    donation_requests = Donation.objects.filter(blood_bank=blood_bank, status='not_confirmed')
    upcoming_donations=Donation.objects.filter(blood_bank=blood_bank, status='pending')
    not_accepted=Donation.objects.filter(blood_bank=blood_bank, status='not_accepted')
    for donation in donation_requests:
        donation.donor_blood_group = NormalUser.objects.get(user=donation.donor).blood_group
    for donation in not_accepted:
        donation.donor_blood_group = NormalUser.objects.get(user=donation.donor).blood_group
    for donation in upcoming_donations:
        donation.donor_blood_group = NormalUser.objects.get(user=donation.donor).blood_group
    count_pending = donation_requests.count()

    user_requests = get_object_or_404(BloodBank, user=request.user)

    if request.method == "POST":
        form = DonationRequestCreationForm(request.POST)
        requested = {
            'a0': Decimal(request.POST.get('a0', user_requests.a0)),
            'a1': Decimal(request.POST.get('a1', user_requests.a1)),
            'b0': Decimal(request.POST.get('b0', user_requests.b0)),
            'b1': Decimal(request.POST.get('b1', user_requests.b1)),
            'ab0': Decimal(request.POST.get('ab0', user_requests.ab0)),
            'ab1': Decimal(request.POST.get('ab1', user_requests.ab1)),
            'o0': Decimal(request.POST.get('o0', user_requests.o0)),
            'o1': Decimal(request.POST.get('o1', user_requests.o1)),
        }
        
        # Update the user_requests instance
        for key, value in requested.items():
            setattr(user_requests, key, value)
        user_requests.save()

        
        if form.is_valid():
            donation_request = form.save(commit=False)  # Don't save to DB yet
            
            # Set the blood_bank to the currently logged-in user's BloodBank
            donation_request.blood_bank = BloodBank.objects.get(user=request.user)
            matching_users = NormalUser.objects.filter(blood_group=donation_request.blood_group)
            
            # Save the donation request
            print(matching_users.count())
            donation_request.sent_requests=matching_users.count()
            donation_request.save()
            # user_id_list = list(matching_users)
            # print(user_id_list)
            fulfilled_request = FulfilledRequests.objects.create(donation_req_id=donation_request.id)
            # fulfilled_request.user_ids.set(user_id_list)
            # print(fulfilled_request)
            
            # Find users with the requested blood group
            
            print(matching_users)
            inline_keyboard = {
                "inline_keyboard": [
                [
                {"text": "Yes", "callback_data": f"yes_{donation_request.id}"},
                {"text": "No", "callback_data": f"no_{donation_request.id}"}
                ]
                ]
                }
            
            message = f'''A donation request for {donation_request.blood_group} has been made by {donation_request.blood_bank} Hospital.
               The {donation_request.blood_bank} Hospital needs {donation_request.requested_amount} ml of {donation_request.blood_group} blood.
               Its Phone number is {donation_request.blood_bank.user.phone_number} and its address is {donation_request.blood_bank.user.address}.
               Please respond if you can donate.'''
            # Send Telegram messages to all matching users
            for user in matching_users:
                
                send_telegram_message(user.user.telegram_chat_id, message,request_contact=False,reply_markup=inline_keyboard)

            # Redirect to the summary page with the request ID
            return redirect('donation_request_summary', request_id=donation_request.id)
    else:
        form = DonationRequestCreationForm()
    percentage_all = {
        'a0': user_requests.calculate_stock_percentage('A-'),
        'a1': user_requests.calculate_stock_percentage('A+'),
        'b0': user_requests.calculate_stock_percentage('B-'),
        'b1': user_requests.calculate_stock_percentage('B+'),
        'ab0': user_requests.calculate_stock_percentage('AB-'),
        'ab1': user_requests.calculate_stock_percentage('AB+'),
        'o0': user_requests.calculate_stock_percentage('O-'),
        'o1': user_requests.calculate_stock_percentage('O+'),
    }
    donations_count={
        'not_confirmed':count_pending,
        'donated':Donation.objects.filter(blood_bank=blood_bank, status='donated').count(),
        'pending':Donation.objects.filter(blood_bank=blood_bank, status='pending').count(),
        'total_stock':user_requests.a0 + user_requests.a1 +user_requests.b0 + user_requests.b1 +user_requests.ab0 + user_requests.ab1 +user_requests.o0 + user_requests.o1,
    }

    return render(request, 'main/blood_bank_dashboard.html', {
        'donation_requests': donation_requests,
        'upcoming_donations': upcoming_donations,
        'not_accepted': not_accepted,
        'form': form,
        'user_requests': user_requests,
        'percentage_all': percentage_all,
        'donations_count':donations_count,
        'blood_bank': blood_bank,
        'donation_requestsss': DonationRequest.objects.filter(blood_bank=blood_bank),
    })

@login_required
def donation_request_summary(request, request_id):
    # Get the specific donation request
    donation_request = get_object_or_404(DonationRequest, id=request_id, blood_bank__user=request.user)

    accepted_request = get_object_or_404(FulfilledRequests, donation_req_id=request_id).fulfilled_by
    fulfilled_request = get_object_or_404(FulfilledRequests, donation_req_id=request_id)
    all_requests = fulfilled_request.user_ids.all()

    if request.method == "POST" and 'mark_fulfilled' in request.POST and donation_request.status == 'pending':
        # Update the status to 'fulfilled'
        fulfilled_request_id = request.POST.get('fulfilled_request_id')
        fulfilled_request.fulfilled_by=get_object_or_404(NormalUser, user__id=fulfilled_request_id)
        fulfilled_request.save()
        get_object_or_404(FulfilledRequests, donation_req_id=request_id).user_ids.remove(NormalUser.objects.get(user__id=fulfilled_request_id))
        donation_request.status = 'fulfilled'
        donation_request.save()
        return redirect('donation_request_summary', request_id=request_id)

    return render(request, 'donations/donation_request_summary.html', {
        'donation_request': donation_request,
        'all_requestss': donation_request.sent_requests,
        'confirmed_request': accepted_request,
        'all_requests': all_requests,
        'request_id': request_id
    })



@login_required
def donation_detail(request, id):
    # Retrieve all donations made by the donor
    donations = get_object_or_404(Donation, id=id)
    donations.donor_blood_group = NormalUser.objects.get(user=donations.donor).blood_group
    try:
        blood_bank = request.user.blood_bank
    except Exception:
        return redirect('home')  # Redirect if user is not a blood bank

    if request.method == "POST":
        print(1)
        form = DonationConfirmationForm(request.POST, instance=donations)
        if form.is_valid():
            form.save()
            return redirect('blood_bank_home')
    else:
        form = DonationConfirmationForm()

    return render(request, 'donations/donation_detail.html', {'donations': donations,'form': form,'blood_bank':blood_bank})

TELEGRAM_BOT_TOKEN = ''

def send_telegram_message(chat_id, message,request_contact=False,reply_markup=None):
    print(request_contact)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    if request_contact==True:
       reply_markup = {
        "keyboard": [
            [
                {
                    "text": "Share my phone number",
                    "request_contact": True
                }
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
       } 
       payload = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": reply_markup
       }
    else:
        payload = {
        "chat_id": chat_id,
        "text": message
        }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    response = requests.post(url, json=payload)
    return response.json()

def send_request_form(request):
    """Render the form to send a blood request using a phone number."""
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            return redirect(reverse('request_blood_by_phone', kwargs={'phone_number': phone_number}))
    return render(request, 'another/send_request.html')

def request_blood_by_phone(request, phone_number):
    """Handle sending a blood request using the user's phone number."""
    user = get_object_or_404(NormalUser, user__phone_number=phone_number)
    
    if not user.user.telegram_chat_id:
        return render(request, 'error.html', {'message': 'User has not registered on Telegram.'})

    message = (
        f"Dear {user.user.username},\n\n"
        f"Urgent request for blood group {user.blood_group} at Mumbai.\n"
        "Can you help by donating blood?"
    )
    
    # Inline keyboard buttons for "Yes" and "No"
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "Yes", "callback_data": f"yes_{user.user.telegram_chat_id}"},
                {"text": "No", "callback_data": f"no_{user.user.telegram_chat_id}"}
            ]
        ]
    }
    
    success = send_telegram_message(
        user.user.telegram_chat_id,
        message,
        request_contact=False,  # Do not request contact sharing
        reply_markup=inline_keyboard  # Pass the inline keyboard
    )

    if success:
        return render(request, 'another/success.html')
    else:
        return render(request, 'another/error.html', {'message': 'Failed to send message via Telegram.'})


def webhook_info(request):
    """Provide instructions for users to connect their Telegram accounts."""
    return render(request, 'another/webhook_info.html')

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            # Log the raw request body for debugging
            print("Raw POST request body:", request.body)

            # Parse JSON payload
            update = json.loads(request.body)
            print("Parsed update:", update)

            # Extract chat ID and user message
            chat_id = update.get('message', {}).get('chat', {}).get('id')
            user_message = update.get('message', {}).get('text')
            contact = update.get('message', {}).get('contact')
            update = json.loads(request.body)

            # Check if it's a callback query
            if "callback_query" in update:
             callback_query = update["callback_query"]
             chat_id = callback_query["message"]["chat"]["id"]
             message_id = callback_query["message"]["message_id"]
             callback_data = callback_query["data"]

             # Process "Yes" or "No" response
             if callback_data.startswith("yes_"):
                # Edit message text to confirm the action and remove buttons
                request_id = callback_data.split("_")[1]
                norm_user=NormalUser.objects.get(user__telegram_chat_id=chat_id)
                fr_object=FulfilledRequests.objects.get(donation_req_id=request_id)
                fr_object.user_ids.add(norm_user)
                edit_message_text(chat_id, message_id, "Thank you for agreeing to help!")
                return JsonResponse({"status": "success"})
             elif callback_data.startswith("no_"):
                # Optionally handle "No" response
                edit_message_text(chat_id, message_id, "No worries! Thank you for your response.")
                return JsonResponse({"status": "success"})

            # Handle contact sharing
            if contact and not NormalUser.objects.filter(user__telegram_chat_id=chat_id).exists():
             phone_number = contact.get('phone_number')
             phone_number = phone_number[3:]  # Remove first 3 characters
             chat_id = contact.get('user_id')
             print(phone_number)
             user = get_object_or_404(NormalUser, user__phone_number=phone_number)
             print(chat_id)
             user.user.telegram_chat_id = chat_id
             print(user.user.telegram_chat_id)
             user.user.save()
             return JsonResponse({"status": "success", "phone_number": phone_number})

            # Handle /start command
            if user_message == '/start':
             send_telegram_message(
                chat_id,
                "Hi! Please share your phone number by clicking the button below:",
                request_contact=True,
                reply_markup=None
             )
             return JsonResponse({"status": "success", "message": "Asked for phone number"})


            if chat_id and user_message:
                # Respond to the user
                reply = f"You said: {user_message}"
                send_telegram_message(chat_id, reply,request_contact=False,reply_markup=None)
                return JsonResponse({"status": "success"})

            return JsonResponse({"status": "error", "message": "Invalid update structure"})
        except Exception as e:
            # Log any errors for debugging
            print("Error processing POST request:", str(e))
            return JsonResponse({"status": "error", "message": str(e)})

    elif request.method == 'GET':
        print("Received a GET request")
        return JsonResponse({"status": "error", "message": "GET requests are not supported"})

    return JsonResponse({"status": "error", "message": "Invalid request method"})

def edit_message_text(chat_id, message_id, new_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_text
    }
    response = requests.post(url, json=payload)
    return response.ok

def haversine_distance(lat1, lon1, lat2, lon2):
    import math
    R = 6371  # Radius of Earth in km

    # Ensure all inputs are floats
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def blood_bank_locator(request):
    return render(request, "main/blood_bank_locator.html")

def find_blood_banks(request):
  if request.method != 'GET':
        sorted_blood_banks = BloodBank.objects.all()
        return render(request,"main/bloodbank_search.html", {'all_requests': sorted_blood_banks})
  else:  
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({"error": "Missing latitude or longitude"}, status=400)

    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        return JsonResponse({"error": "Invalid latitude or longitude"}, status=400)

    blood_banks_data= list(BloodBank.objects.all())
    
    # Calculate distances and sort by nearest
    for bank in blood_banks_data:
        bank["distance"] = haversine_distance(lat, lon, bank["lat"], bank["lon"])

    sorted_blood_banks = sorted(blood_banks_data, key=lambda x: x["distance"])

  return render(request,"main/bloodbank_search.html", {'all_requests': sorted_blood_banks})


from django.shortcuts import render
import json

def bbsearch(request):
    user111 = get_object_or_404(NormalUser, user=request.user)
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from the request
            lat = data.get('lat')
            lon = data.get('lon')

            if not lat or not lon:
                return JsonResponse({"error": "Missing latitude or longitude"}, status=400)

            lat, lon = float(lat), float(lon)

            # Fetch blood banks
            blood_banks = BloodBank.objects.all()
            blood_banks_data = [
                {
                    "name": bank.organization_name,
                    "lat": bank.user.loc_latitude,
                    "lon": bank.user.loc_longitude,
                    "address": bank.user.address,
                    "phone_number": bank.user.phone_number,
                    "email": bank.user.email,
                    "id":bank.id,
                }
                for bank in blood_banks
            ]

            # Calculate distances and sort by nearest
            for bank in blood_banks_data:
                bank["distance"] = haversine_distance(lat, lon, bank["lat"], bank["lon"])

            sorted_blood_banks = sorted(blood_banks_data, key=lambda x: x["distance"])

            # Pass the sorted data to the template
            return render(request, "main/bloodbank_search.html", {'all_requests': sorted_blood_banks, 'user111': user111})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Render default template for GET requests
    return render(request, "main/bloodbank_search.html", {'all_requests': BloodBank.objects.all(), 'user111': user111})

from decimal import Decimal

def blood_bank_profile(request, bank_id):
    user_requests = get_object_or_404(BloodBank, id=bank_id)
    blood_bank=user_requests
    donation_requests = Donation.objects.filter(blood_bank=user_requests, status='not_confirmed')
    upcoming_donations=Donation.objects.filter(blood_bank=user_requests, status='pending')
    for donation in upcoming_donations:
        donation.donor_blood_group = NormalUser.objects.get(user=donation.donor).blood_group
    count_pending = donation_requests.count()
    donations_count={
        'not_confirmed':count_pending,
        'donated':Donation.objects.filter(blood_bank=user_requests, status='donated').count(),
        'pending':Donation.objects.filter(blood_bank=user_requests, status='pending').count(),
        'total_stock':user_requests.a0 + user_requests.a1 +user_requests.b0 + user_requests.b1 +user_requests.ab0 + user_requests.ab1 +user_requests.o0 + user_requests.o1,
    }

    percentage_all = {
        'a0': user_requests.calculate_stock_percentage('A-'),
        'a1': user_requests.calculate_stock_percentage('A+'),
        'b0': user_requests.calculate_stock_percentage('B-'),
        'b1': user_requests.calculate_stock_percentage('B+'),
        'ab0': user_requests.calculate_stock_percentage('AB-'),
        'ab1': user_requests.calculate_stock_percentage('AB+'),
        'o0': user_requests.calculate_stock_percentage('O-'),
        'o1': user_requests.calculate_stock_percentage('O+'),
    }
    context = {
        'user_requests': user_requests,
        'donation_requests': donation_requests,
        'upcoming_donations': upcoming_donations,
        'percentage_all': percentage_all,
        'donations_count':donations_count,
        'blood_bank': blood_bank,
    }
    return render(request, 'main/blood_bank_profile1111.html', context)

def update_max_capacity(request):
    if request.method == 'POST':
        max_capacity = request.POST.get('max_capacity')
        blood_bank = get_object_or_404(BloodBank, user=request.user)
        max_cap=max(blood_bank.a0,blood_bank.a1,blood_bank.b0,blood_bank.b1,blood_bank.ab0,blood_bank.ab1,blood_bank.o0,blood_bank.o1)
        if int(max_capacity) < max_cap:
            messages.error(request, 'Max capacity cannot be less than current stock!')
            return redirect('blood_bank_home')
        blood_bank.max_capacity_per_group = int(max_capacity)
        try:
          blood_bank.save()
          messages.success(request, 'Max capacity updated successfully!')
          return redirect('blood_bank_home')
        except Exception as e:
          print(e)
          messages.error(request, f'Error updating max capacity: {str(e)}')
          return redirect('blood_bank_home')
    return redirect('blood_bank_home')

@login_required
def view_profile(request):
    if request.user.user_type == 'normal':
        user111 = get_object_or_404(NormalUser, user=request.user)
        home='normal'
    else:
        user111 = get_object_or_404(BloodBank, user=request.user)
        home='blood_bank'

    if request.method == 'POST':
        # Handle profile update logic here
        # For example, you can update the user's phone number or address
        user111.user.username = request.POST.get('username', user111.user.username)
        user111.user.email = request.POST.get('email', user111.user.email)
        user111.user.phone_number = request.POST.get('phone_number', user111.user.phone_number)
        user111.user.address = request.POST.get('address', user111.user.address)
        user111.user.city = request.POST.get('city', user111.user.city)
        user111.user.state = request.POST.get('state', user111.user.state)
        user111.user.pincode = request.POST.get('pincode', user111.user.pincode)
        user111.user.loc_latitude = request.POST.get('latitude', user111.user.loc_latitude)
        user111.user.loc_longitude = request.POST.get('longitude', user111.user.loc_longitude)
        user111.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('view_profile')
    return render(request, 'main/profile_page.html', {'user111': user111,'home':home})

    