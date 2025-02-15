from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Clothes(models.Model):
    SIZES = (
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),  # Changed 'large' to 'Large'
    )
    
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100, choices=SIZES)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.name
    
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
class Store(models.Model): 
    clothes = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    clothes_varieties = models.ManyToManyField(Clothes, related_name="stores")
    
    def __str__(self):
        return self.location
    
class ClothesCertification(models.Model):
    name = models.OneToOneField(Clothes, on_delete=models.CASCADE)
    certification = models.CharField(max_length=100)
    
    def __str__(self): 
        return f'Certificate for {self.name.name}'
