from django.db import models
from django.contrib.auth.models import User

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

# user model is here

class customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    phone_field = models.CharField(max_length=10, blank=False)
    
    def __str__(self):
        return self.user.username   
