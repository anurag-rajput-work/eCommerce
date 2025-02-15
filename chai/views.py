from django.shortcuts import render
from django.http import HttpResponse
from .models import Clothes
# Create your views here.
def myapp(request):
    cloth =  Clothes.objects.all()
    return render(request, 'chai/my_app.html',{'cloth':cloth})