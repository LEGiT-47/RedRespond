
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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Save additional fields
            if user.user_type == 'blood_bank':
                BloodBank.objects.create(
                    user=user,
                    organization_name=form.cleaned_data['organization_name'],
                )
                login(request, user)
                return redirect('blood_bank_home')  # Redirect blood bank users to their home
            elif user.user_type == 'normal':
                NormalUser.objects.create(
                    user=user,
                    blood_group=form.cleaned_data['blood_group'],
                )
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
    blood_groupiee=NormalUser.objects.get(user=request.user)
    # past_donations = Donation.objects.filter(donor=request.user).exclude(status='not_confirmed',status='not_accepted')
    already = Donation.objects.filter(donor=request.user,  status='donated')
    notconfirm= Donation.objects.filter(donor=request.user,status='not_confirmed')
    pending= Donation.objects.filter(donor=request.user, scheduled_datetime__gt=timezone.now(),status='pending')
    if request.method == "POST":
        form = DonationRequestForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user  # Automatically set donor from logged-in user
            donation.save()
            return redirect('donation_request_success')
    else:
          form = DonationRequestForm()
    return render(request, 'main/normal_home.html', {'form': form,'blood_groupiee':blood_groupiee,'already':already,'notconfirm':notconfirm,'pending':pending})

def logout_view(request):
    logout(request)
    return redirect('login')

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
    past_donations = Donation.objects.filter(donor=request.user, confirmed=True)
    return render(request, 'donations/past_donations.html', {'past_donations': past_donations})

@login_required
def blood_donation_page(request,id):
    donation = get_object_or_404(Donation, id=id)
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
    if request.method == "POST":
        form = DonationRequestCreationForm(request.POST)

        
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
               The {donation_request.blood_bank} Hospital needs {donation_request.requested_amount} units of {donation_request.blood_group} blood.
               Its Phone number is {donation_request.blood_bank.user.phone_number} and its address is {donation_request.blood_bank.user.address}.
               Please respond if you can donate.'''
            # Send Telegram messages to all matching users
            for user in matching_users:
                
                send_telegram_message(user.user.telegram_chat_id, message,request_contact=False,reply_markup=inline_keyboard)

            # Redirect to the summary page with the request ID
            return redirect('donation_request_summary', request_id=donation_request.id)

    
    else:
        form = DonationRequestCreationForm()

    return render(request, 'main/blood_bank_home.html', {
        'donation_requests': donation_requests,
        'form': form
    })

@login_required
def donation_request_summary(request, request_id):
    # Get the specific donation request
    donation_request = get_object_or_404(DonationRequest, id=request_id, blood_bank__user=request.user)

    accepted_request = get_object_or_404(FulfilledRequests, donation_req_id=request_id).fulfilled_by
    fulfilled_request = get_object_or_404(FulfilledRequests, donation_req_id=request_id)
    all_requests = fulfilled_request.user_ids.all()

    if request.method == "POST" and 'mark_fulfilled' in request.POST:
        # Update the status to 'fulfilled'
        donation_request.status = 'fulfilled'
        donation_request.save()
        return redirect('donation_request_summary', request_id=request_id)

    return render(request, 'donations/donation_request_summary.html', {
        'donation_request': donation_request,
        'all_requestss': donation_request.sent_requests,
        'confirmed_request': accepted_request,
        'all_requests': all_requests
    })



@login_required
def donation_detail(request, id):
    # Retrieve all donations made by the donor
    donations = get_object_or_404(Donation, id=id)

    if request.method == "POST":
        print(1)
        form = DonationConfirmationForm(request.POST, instance=donations)
        if form.is_valid():
            form.save()
            return redirect('blood_bank_home')
    else:
        form = DonationConfirmationForm()

    return render(request, 'donations/donation_detail.html', {'donations': donations,'form': form})

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
             phone_number = phone_number[2:]  # Remove first 3 characters
             chat_id = contact.get('user_id')
             user = get_object_or_404(NormalUser, user__phone_number=phone_number)
             print(chat_id)
             user.user.telegram_chat_id = chat_id
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
