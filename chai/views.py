from django.shortcuts import render
from django.http import HttpResponse
from .models import Clothes
from django.shortcuts import get_object_or_404
from .forms import clothesForm
# Create your views here.
def myapp(request):
    cloth =  Clothes.objects.all()
    return render(request, 'chai/my_app.html',{'cloth':cloth})

def detail(request, clothes_id):
    cloth = get_object_or_404(Clothes, pk=clothes_id)
    return render(request, 'chai/detail.html', {'cloth':cloth})
def clothes_store(request):
    store = None
    form = clothesForm()  # Initialize the form
    if request.method == 'POST':
        form = clothesForm(request.POST)  
        if form.is_valid():
            varity = form.cleaned_data['store']
            store = Clothes.objects.filter(clothes_varieties=varity)
    return render(request, 'chai/clothes_store.html', {'store': store, 'form': form}) 