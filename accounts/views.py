from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from chai.models import customer
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Welcome back.")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('user_login') 
    else:
        return render(request, 'accounts/login.html') 


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Choose a different one.")
                return redirect('user_register')
            else :
                if User.objects.filter(email=email).exists():
                    messages.error(request, "email already exists. Choose a different one.")
                    return redirect('user_register')
                else :
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    
                    # code for login
                    
                    data = customer(user=user, phone_field=phone)
                    data.save()
                    
                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        messages.success(request, "Registration successful! Welcome to Online clothe shop.")
                        return redirect('/')
            return redirect('user_register')
        else:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('user_register')
    else:
        return render(request, 'accounts/register.html')

def user_logout(request):
    logout(request)
    return redirect('/')
