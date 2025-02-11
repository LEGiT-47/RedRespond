from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BloodBank, NormalUser, Donation


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
    organization_name = forms.CharField(max_length=255, required=False)
    blood_group = forms.CharField(max_length=5, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2', 'user_type',
            'phone_number', 'address', 'city', 'state', 'pincode',
            'organization_name', 'blood_group',
        ]

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        organization_name = cleaned_data.get('organization_name')
        blood_group = cleaned_data.get('blood_group')

        if user_type == 'blood_bank' and not organization_name:
            self.add_error('organization_name', 'This field is required for Blood Banks.')
        elif user_type == 'normal' and not blood_group:
            self.add_error('blood_group', 'This field is required for Normal Users.')




class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['blood_bank', 'donated_amount', 'scheduled_datetime']
        widgets = {
            'scheduled_datetime': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full px-4 py-3 rounded border border-gray-200 focus:border-red-500 focus:ring focus:ring-red-200 transition duration-300'
                }
            ),
            'donated_amount': forms.NumberInput(
                attrs={
                    'class': 'w-full px-4 py-3 rounded border border-gray-200 focus:border-red-500 focus:ring focus:ring-red-200 transition duration-300',
                    'placeholder': 'Enter amount donated'
                }
            ),
            'blood_bank': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 rounded border border-gray-200 focus:border-red-500 focus:ring focus:ring-red-200 transition duration-300'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the blood bank dropdown to all registered blood banks.
        self.fields['blood_bank'].queryset = BloodBank.objects.all()
        self.fields['donated_amount'].label = "Amount Donated (units)"
        self.fields['scheduled_datetime'].label = "Select Donation Date & Time"

class DonationConfirmationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['confirmed']
