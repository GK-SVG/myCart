from django.shortcuts import render,redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'MJs5tlGfwOMzMTQ@'
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
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html',{'thank': thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception :
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.pro_desc.lower() or query in item.pro_name.lower() or query in item.categary.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('categary', 'id')
    cats = {item['categary'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(categary=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)
    

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        id = order.order_id
        param_dict = {

                'MID': 'toaldV34834751882298',
                'ORDER_ID': str(id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order success full')
        else:
            #order_success=messages.error(request,f'order was not successful because {response_dict[RESPMSG]}')
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict,'order_success':order_success})

def prodView(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email=request.POST['email']
        password=request.POST['pass1']
        password2=request.POST['pass2']

        # checkpoints 
        #username length checker
        if len(username) > 12 :
            messages.error(request,'Username must have maximum 12 Charcters Please try again')
            return redirect('/shop')

        # username charkters checker
        if not username.isalnum() :
             messages.error(request,'Username only contain alphaNumeric value Please try again')
             return redirect('/shop')       

        # password1 and password2 checker     
        if password != password2 :
            messages.error(request,'Passwords do not match Please try again')
            return redirect('/shop')
        # creating user
        try:
            myuser=User.objects.get(username=username)
            messages.error(request,'The username you entered has already been taken. Please try another username.')
            return redirect('/shop')
        except:
            myuser = User.objects.create_user(username=username,email=email,password=password)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            messages.success(request,'Your account created succesfully')
            return redirect('/shop')
    else:
        return HttpResponse('404 - Not Found')


def handlelogin(request):
    if request.method == "POST":
        username = request.POST["loginusername"]
        password = request.POST["loginpassword"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect('/shop')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('/shop')
    else:
        return HttpResponse('Error Not Found 404')

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/shop')