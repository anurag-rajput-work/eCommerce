from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Clothes
from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib import messages
# Create your views here.
def myapp(request):
    cloth =  Clothes.objects.all()
    return render(request, 'chai/my_app.html',{'cloth':cloth})

def detail(request, clothes_id):
    cloth = get_object_or_404(Clothes, pk=clothes_id)
    return render(request, 'chai/detail.html', {'cloth':cloth})
def add_product(request):
    if request.method == "POST":
        form = ClothesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("add_product")
    else:
        form = ClothesForm()
    return render(request, "chai/add_product.html", {"form": form})