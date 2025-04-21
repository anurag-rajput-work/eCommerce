from django.contrib import admin
from chai.models import *


# Register your models here

class ClothesReviewAdmin(admin.TabularInline):
    model = ClothesReview
    extra = 2

class clothesAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'quantity')
    inlines = [ClothesReviewAdmin]
    
class StoreAdmin(admin.ModelAdmin):
    list_display = ('clothes', 'location')  
    filter_horizontal = ('clothes_varieties',)

class ClothesCertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'certification',) 

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_field', 'id')  # Use the existing id field instead


admin.site.register(Clothes, clothesAdmin)
admin.site.register(ClothesCertification, ClothesCertificationAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(customer, CustomerAdmin) 
admin.site.register(order_Item)
admin.site.register(Order)
admin.site.register(CheckoutDetails)