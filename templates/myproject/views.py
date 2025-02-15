from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def contact(request):
    return HttpResponse("Hello,  this is my contact page")

def about(request):
    return HttpResponse("hello, This is our about page")

