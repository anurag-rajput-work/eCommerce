from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from chai.models import customer

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, '/', {'message': 'Login successful!'})
        else:
            return render(request, 'accounts/login.html', {'message': 'Invalid credentials!'})
    else:
        return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')
        if confirm_password == password:
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/register.html', {'message': 'Username already exists!'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'accounts/register.html', {'message': 'Email already exists!'})
            else:
                user = User.objects.create_user(username=username, email=email, password=password, phone=phone)
                User.save()
                
                data = customer(user=user, phone_field=phone)
                data.save()
                
                our_user = authenticate(username=username, password=password)
                if our_user is not None:
                    login(request, user)
                    return render(request, '/', {'message': 'Registration successful!'})
    else:
        return render(request, 'accounts/register.html')

def user_logout(request):
    pass
