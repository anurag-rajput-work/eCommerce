
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.myapp, name='home'),
    path('<int:clothes_id>/', views.detail, name='detail'),
    path('add_product/', views.add_product, name='add_product'),
]
