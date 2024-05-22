from django import forms
from .models import Membership
from django.shortcuts import render, redirect
from .models import KickboxingRegistration
from .models import ZumbaRegistration
from .models import CrossfitRegistration
from .models import YogaRegistration
from django.contrib.auth.forms import AuthenticationForm
from .models import Trainer
from .models import FreePassRequest


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = [
            'first_name',
            'last_name',
            'address',
            'age',
            'gender',
            'phone_number',
            'date_of_joining',
        ]

        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }


    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) < 10:
            raise forms.ValidationError('Phone number should be at least 10 digits.')
        return phone_number

class KickboxingRegistrationForm(forms.ModelForm):
    class Meta:
        model = KickboxingRegistration
        fields = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number','payment_option' ]

class ZumbaRegistrationForm(forms.ModelForm):
    class Meta:
        model = ZumbaRegistration
        fields = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number','payment_option' ]

class CrossfitRegistrationForm(forms.ModelForm):
    class Meta:
        model = CrossfitRegistration
        fields = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number','payment_option' ]

class YogaRegistrationForm(forms.ModelForm):
    class Meta:
        model = YogaRegistration
        fields = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number', 'payment_option']

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['full_name', 'age', 'gender', 'email', 'address', 'phone_number']

class FreePassRequestForm(forms.ModelForm):
    class Meta:
        model = FreePassRequest
        fields = ['full_name', 'age', 'phone_number', 'email', 'trial_date']

