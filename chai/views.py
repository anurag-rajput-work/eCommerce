from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import * 
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib import messages
from django.utils import timezone
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Initialize razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def myapp(request):
    cloth =  Clothes.objects.all()
    return render(request, 'chai/my_app.html',{'cloth':cloth})

def detail(request, pk):
    cloth = get_object_or_404(Clothes, pk=pk)
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

@login_required
def add_to_cart(request, pk):
    cloth = Clothes.objects.get(pk=pk)
    
    order_item, created = order_Item.objects.get_or_create(
        user=request.user,
        clothes=cloth,  
        ordered=False,
    )
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(clothes__pk=pk).exists():  
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("detail", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("detail", pk=pk)

@login_required
def cart(request):
    try:
        if not request.user.is_authenticated:
            messages.warning(request, "Please login to view your cart.")
            return redirect("login")
            
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        
        if order_qs.exists():
            order = order_qs.first()
            if order.items.count() > 0:
                return render(request, "chai/cart.html", {"order": order})
            else:
                messages.info(request, "Your cart is empty.")
                return render(request, "chai/cart.html", {"order": None})
        else:
            messages.info(request, "Your cart is empty.")
            return render(request, "chai/cart.html", {"order": None})
            
    except Exception as e:
        messages.error(request, "An error occurred while loading your cart.")
        return render(request, "chai/cart.html", {"order": None})

@login_required
def add_item(request, pk):
    cloth = Clothes.objects.get(pk=pk)
    
    order_item, created = order_Item.objects.get_or_create(
        user=request.user,
        clothes=cloth,
        ordered=False,
    )
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(clothes__pk=pk).exists():  
            if order_item.quantity < cloth.quantity:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("cart")
            else:
                messages.info(request, "This item is out of stock.")
                return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart")
    
@login_required
def remove_item(request, pk):
    cloth = get_object_or_404(Clothes, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(clothes__pk=pk).exists():
            order_item = order.items.get(clothes=cloth, user=request.user, ordered=False)
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
            return redirect("cart")
    messages.info(request, "This item was not in your cart.")
    return redirect("cart")

@login_required
def delete_item(request, pk):
    cloth = get_object_or_404(Clothes, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(clothes=cloth).exists():
            order_item = order.items.get(clothes=cloth)
            order.items.remove(order_item)
            order_item.delete() 
            messages.success(request, f"{cloth.name} was removed from your cart.")
        else:
            messages.info(request, "This item was not in your cart.")
    else:
        messages.info(request, "You do not have an active order.")
    
    return redirect("cart")


@login_required
def checkout_view(request):
    # Check if user has an active order
    current_order = Order.objects.filter(user=request.user, ordered=False).first()
    
    # If no active order, redirect to cart
    if not current_order:
        messages.warning(request, "You don't have any items in your cart.")
        return redirect("cart")
    
    # Check if user already has checkout details for current order
    if CheckoutDetails.objects.filter(user=request.user, order=current_order).exists():
        messages.info(request, "You have already completed checkout for this order.")
        return redirect("cart")
        
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        
        try:
            if form.is_valid():
                name = form.cleaned_data.get("name")
                contact_number = form.cleaned_data.get("contact_number")
                house_number = form.cleaned_data.get("house_number")
                area = form.cleaned_data.get("area")
                city = form.cleaned_data.get("city")
                state = form.cleaned_data.get("state")
                pin_code = form.cleaned_data.get("pin_code")
                country = form.cleaned_data.get("country")
                same_billing_address = form.cleaned_data.get("same_billing_address")
                
                # Get the current order
                order = Order.objects.get(user=request.user, ordered=False)
                
                # Create shipping address string
                shipping_address = f"{house_number}, {area}, {city}, {state}, {pin_code}, {country}"
                
                # Save shipping address to order
                order.shipping_address = shipping_address
                if same_billing_address:
                    order.billing_address = shipping_address
                
                # Mark the order as completed
                order.ordered = True
                order.save()
                
                # Mark all order items as ordered
                order.items.all().update(ordered=True)
                
                # Create checkout details
                checkout = CheckoutDetails(
                    user=request.user,
                    order=order,
                    name=name,
                    contact_number=contact_number,
                    house_number=house_number,
                    area=area,
                    city=city,
                    state=state,
                    pin_code=pin_code,
                    country=country,
                    same_billing_address=same_billing_address,
                )
                checkout.save()
                
                messages.success(request, "Your order has been placed successfully!")
                return redirect("cart")
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("cart")
    else:
        form = CheckoutForm()
    return render(request, "chai/checkout.html", {"form": form})

@login_required           
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        cloth = Clothes.objects.filter(name__contains=searched)
        return render(request, 'chai/search.html', 
        {'searched':searched,
        'cloth':cloth})
    else:
        return render(request, 'chai/search.html', {})

@login_required
def initiate_payment(request):
    try:
        # Get the current order
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if not order_qs.exists():
            messages.warning(request, "You don't have any items in your cart.")
            return redirect("cart")
        
        order = order_qs[0]
        amount = int(order.get_total() * 100)  # Convert to paise
        
        # Create a Razorpay Order
        razorpay_order = client.order.create(dict(
            amount=amount,
            currency='INR',
            payment_capture='0'
        ))
        
        # Save the order ID in your database
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        # Prepare context for template
        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'currency': 'INR',
            'callback_url': 'http://' + request.get_host() + '/paymenthandler/'
        }
        
        return render(request, 'chai/payment.html', context)
        
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("cart")

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            # Get the required parameters from post request
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            result = client.utility.verify_payment_signature(params_dict)
            
            if result is not None:
                try:
                    # Get the order
                    order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                    
                    # Capture the payment
                    amount = int(order.get_total() * 100)
                    client.payment.capture(payment_id, amount)
                    
                    # Update the order status
                    order.ordered = True
                    order.payment_id = payment_id
                    order.save()
                    
                    # Clear the cart
                    order.items.all().update(ordered=True)
                    
                    messages.success(request, "Payment successful! Your order has been placed.")
                    return redirect("cart")
                    
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect("cart")
            else:
                messages.error(request, "Payment verification failed.")
                return redirect("cart")
                
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("cart")
    else:
        return HttpResponseBadRequest()


