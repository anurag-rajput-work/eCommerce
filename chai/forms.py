from django import forms
from .models import Clothes

class clothesForm(forms.Form):
    clothes_store = forms.ModelChoiceField(queryset=Clothes.objects.all(), label='Name of Clothes')

