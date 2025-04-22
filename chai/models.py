from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import random


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @staticmethod
    def get_default_category():
        category, created = Category.objects.get_or_create(name="Uncategorized")
        return category.id


# clothes models is here
class Clothes(models.Model):
    SIZES = (
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),  
    )
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= Category.get_default_category)
    size = models.CharField(max_length=100, choices=SIZES)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(default='')
    
    def __str__(self):
        return self.name
    
#review models
class ClothesReview(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = (
        (1, "one"), (2, "two"), (3, "three"), (4, "four"), (5, "five")
    )
    
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=points)
    
    def __str__(self):
        return f'{self.user.username} - {self.clothes.name}'
    
# store model
class Store(models.Model): 
    clothes = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    clothes_varieties = models.ManyToManyField(Clothes, related_name="stores")
    
    def __str__(self):
        return self.location
    
# certification model   
class ClothesCertification(models.Model):
    name = models.OneToOneField(Clothes, on_delete=models.CASCADE)
    certification = models.CharField(max_length=100)
    
    def __str__(self): 
        return f'Certificate for {self.name.name}'


class customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    phone_field = models.CharField(max_length=10, blank=False)
    id = models.AutoField(primary_key=True)  # Adding unique ID field
    
    def __str__(self):
        return self.user.username   


        
class order_Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.quantity} of {self.clothes.name}'
    
    def get_total_item_price(self):
        return self.quantity * self.clothes.price
    
    def get_final_price(self):
        return self.get_total_item_price()
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(order_Item)
    order_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    DateTime_ofpayment = models.DateTimeField(default=timezone.now)
    ordered_delivered = models.BooleanField(default=False)
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            # Get the customer instance for the user
            try:
                customer_instance = customer.objects.get(user=self.user)
                customer_id = customer_instance.id
            except customer.DoesNotExist:
                customer_id = 0  # Default if no customer found
            
            # Generate order ID using timestamp, customer ID and a random component
            timestamp = self.DateTime_ofpayment.strftime("%Y%m%d%H%M%S")
            random_component = random.randint(1000, 9999)
            self.order_id = f"ECOM2{timestamp}{customer_id}{random_component}"
            
            # Ensure uniqueness by checking if the order_id already exists
            while Order.objects.filter(order_id=self.order_id).exists():
                random_component = random.randint(1000, 9999)
                self.order_id = f"ECOM2{timestamp}{customer_id}{random_component}"
            
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
    
    def get_total_count(self):
        return self.items.count()

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class CheckoutDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    contact_number = models.CharField(max_length=15)
    house_number = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    same_billing_address = models.BooleanField(default=True)

    def get_full_address(self):
        return f"{self.house_number}, {self.area}, {self.city}, {self.state}, {self.pin_code}, {self.country}"

    def __str__(self):
        return f"{self.name} - {self.get_full_address()}"
