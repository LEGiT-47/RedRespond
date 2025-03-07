
from .forms import CustomUserCreationForm
from .models import BloodBank, NormalUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from .models import Donation
from .forms import DonationRequestForm, DonationConfirmationForm
from django.utils import timezone

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
    past_donations = Donation.objects.filter(donor=request.user, confirmed=True)
    already = Donation.objects.filter(donor=request.user, confirmed=True, scheduled_datetime__lt=timezone.now())
    notconfirm= Donation.objects.filter(donor=request.user, confirmed=False)
    pending= Donation.objects.filter(donor=request.user, confirmed=True, scheduled_datetime__gt=timezone.now())
    if request.method == "POST":
        form = DonationRequestForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user  # Automatically set donor from logged-in user
            donation.save()
            return redirect('donation_request_success')
    else:
          form = DonationRequestForm()
    return render(request, 'main/normal_home.html', {'form': form,'blood_groupiee':blood_groupiee,'past_donations': past_donations,'already':already,'notconfirm':notconfirm,'pending':pending})

@login_required
def blood_bank_home(request):
    return render(request, 'main/blood_bank_home.html')



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

    donation_requests = Donation.objects.filter(blood_bank=blood_bank, confirmed=False)

    # For each donation, we can handle a confirmation form.
    if request.method == "POST":
        donation_id = request.POST.get('donation_id')
        donation = get_object_or_404(Donation, id=donation_id, blood_bank=blood_bank)
        form = DonationConfirmationForm(request.POST, instance=donation)
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