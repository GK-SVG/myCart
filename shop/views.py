from django.shortcuts import render
from .models import Product
from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # all_pro=[[products,range(1,nSlides),nSlides],
    #          [products,range(nSlides),nSlides]]
    all_pro = []
    catprods = Product.objects.values('categary')
    cats = {item['categary'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(categary=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        all_pro.append([prod, range(1, nSlides), nSlides])

    params = {'all_pro': all_pro}
    #params = {'no_of_slides':nSlides, 'range': range(nSlides),'product': products}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return HttpResponse("We are at contact")

def tracker(request):
    return HttpResponse("We are at tracker")

def search(request):
    return HttpResponse("We are at search")

def checkout(request):
    return HttpResponse("We are at checkout")
