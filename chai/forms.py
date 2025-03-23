from django import forms
from .models import Clothes

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


