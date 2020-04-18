from django.shortcuts import render
from .models import Product
from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    all_pro = []
    catprods = Product.objects.values('categary')
    cats = {item['categary'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(categary=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        all_pro.append([prod, range(1, nSlides), nSlides])

    params = {'all_pro': all_pro}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
   return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def checkout(request):
    return render(request, 'shop/checkout.html/')

def prodView(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})