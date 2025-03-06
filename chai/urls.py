
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.myapp, name='home'),
    path('<int:clothes_id>/', views.detail, name='detail'),
    path('stores/', views.clothes_store, name='store_details'), 
]
