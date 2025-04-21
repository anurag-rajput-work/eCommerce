
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.myapp, name='home'),
    path('product_desc/<pk>', views.detail, name='detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('add_item/<int:pk>', views.add_item, name='add_item'),
    path('remove_item/<int:pk>', views.remove_item, name='remove_item'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout_view, name='checkout'),
]
