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
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS)

    class Meta:
        model = Donation
        fields = ['blood_bank', 'blood_group', 'donated_amount', 'scheduled_datetime', 'additional_info']
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
            'placeholder': 'Enter amount donated',
            'step': '10'
            }
            ),
            'blood_bank': forms.Select(
            attrs={
            'class': 'w-full px-4 py-3 rounded border border-gray-200 focus:border-red-500 focus:ring focus:ring-red-200 transition duration-300'
            }
            ),
            'additional_info': forms.Textarea(
            attrs={
            'class': 'w-full px-4 py-3 rounded border border-gray-200 focus:border-red-500 focus:ring focus:ring-red-200 transition duration-300',
            'rows': 7,
            'placeholder': 'Enter any additional information'
            }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the blood bank dropdown to all registered blood banks.
        self.fields['blood_bank'].queryset = BloodBank.objects.all()
        self.fields['donated_amount'].label = "Amount Donated (units)"
        self.fields['scheduled_datetime'].label = "Select Donation Date & Time"
        self.fields['blood_group'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded border border-gray-200 focus:border-red-500 focus:ring focus:ring-red-200 transition duration-300'
        })

class DonationConfirmationForm(forms.ModelForm):

        

        class Meta:
            model = Donation
            fields = ['status', 'not_accepted_reason']
            widgets = {
                'status': forms.Select(choices=[
                    ('pending', 'Pending'),
                    ('not_accepted', 'Not Accepted')
                ])
            }
            not_accepted_reason = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'rows': 3}),
            help_text='Required if donation is not accepted'
        )

        def clean(self):
            cleaned_data = super().clean()
            status = cleaned_data.get('status')
            not_accepted_reason = cleaned_data.get('not_accepted_reason')

            if status == 'not_accepted' and not not_accepted_reason:
                self.add_error('not_accepted_reason', 'Please provide a reason for not accepting the donation.')
            
            return cleaned_data
