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

    

admin.site.register(Clothes, clothesAdmin)
admin.site.register(ClothesCertification, ClothesCertificationAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(customer)