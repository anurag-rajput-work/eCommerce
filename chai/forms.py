from django import forms
from .models import *

class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ["name", "category", "size", "quantity", "price", "image", "description"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"}),
            "category": forms.Select(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"}),
            "size": forms.Select(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"}),
            "quantity": forms.NumberInput(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"}),
            "price": forms.NumberInput(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none", "step": "0.01"}),
            "image": forms.ClearableFileInput(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"}),
            "description": forms.Textarea(attrs={"class": "w-full mt-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none", "rows": 3}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutDetails
        fields = ['name', 'contact_number', 'house_number', 'area', 'city', 'state', 'pin_code', 'country', 'same_billing_address']
        exclude = ['user', 'order']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter your full name'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter 10-digit mobile number'
            }),
            'house_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter house/apartment number'
            }),
            'area': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter area/locality'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter city name'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter state name'
            }),
            'pin_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter 6-digit PIN code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600',
                'placeholder': 'Enter country name'
            }),
            'same_billing_address': forms.CheckboxInput(attrs={
                'class': 'mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-600 rounded'
            }),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit() or len(contact_number) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit contact number")
        return contact_number

    def clean_pin_code(self):
        pin_code = self.cleaned_data.get('pin_code')
        if not pin_code.isdigit() or len(pin_code) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit PIN code")
        return pin_code