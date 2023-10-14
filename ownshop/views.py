from tkinter import N
from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth import authenticate,login,logout
from E_commerce.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password 


# Create your views here.

def home(request):
    allprods = []
    catprods = Product.objects.values('product_sub_catagory')
    cats = {item['product_sub_catagory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_sub_catagory = cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod,range(1,nslides),nslides])
    params = {'allprods':allprods}
    return render(request,'ownshop/home.html',params)

def faishion(request):
    prod = Product.objects.filter(product_catagory='Fashion Product')
    d = {'prod':prod}
    return render(request,'ownshop/faishion.html',context=d)

def electronics(request):
    prod = Product.objects.filter(product_catagory='Electronics Product')
    d = {'prod':prod}
    return render(request,'ownshop/electronics.html',context=d)

def about(request):
    return render(request,'ownshop/about.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name= name,email= email,phone= phone,desc= desc)
        contact.save()
    return render(request,'ownshop/contact_us.html')


def login_view(request):
    if request.method == 'POST':
        allprods = []
        catprods = Product.objects.values('product_sub_catagory')
        cats = {item['product_sub_catagory'] for item in catprods}
        for cat in cats:
            prod = Product.objects.filter(product_sub_catagory = cat)
            n = len(prod)
            nslides = n // 4 + ceil((n / 4) - (n // 4))
            allprods.append([prod,range(1,nslides),nslides])
            params = {'allprods':allprods}
        email = request.POST.get('email')
        password = request.POST.get('pass')
        u = authenticate(request,username=email,password=password)
        if u is not None:
            login(request,u)
            return render(request,'ownshop/home.html',params)
    return render(request,'ownshop/login.html')


def logout_view(request):
    logout(request=request)
    allprods = []
    catprods = Product.objects.values('product_sub_catagory')
    cats = {item['product_sub_catagory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_sub_catagory = cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod,range(1,nslides),nslides])
        params = {'allprods':allprods}
    return render(request,'ownshop/home.html',params)


def product_details(request,myid):
    product = Product.objects.filter(id= myid)
    return render(request,'ownshop/product_details.html',{'product':product[0]})


def registration(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        repassword = request.POST.get('repass')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        u = User()
        u.email = email
        u.first_name = fname
        u.last_name = lname
        u.mobile = mobile
        if password == repassword:
            u.password = make_password(password)
        u.address = address
        u.save()
        return render(request,'ownshop/login.html')
    return render(request,'ownshop/registration.html')


def checkout(request):
    return render(request, "ownshop/checkout.html")


def payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        items_json = request.POST.get('itemsjson')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        mobile = request.POST.get('mobile')
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        provider_order_id = razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=provider_order_id,items_json=items_json,
            email=email,address=address,city=city,state=state,zip_code=zip_code,mobile=mobile
        )
        order.save()
        return render(
            request,
            "ownshop/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                "razorpay_key": RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    return render(request, "ownshop/payment.html")


@csrf_exempt
def callback(request):       
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = True
            order.save()
            thank = True
            id = order.provider_order_id
            # return render(request, 'ownshop/checkout.html',)
            return render(request, "ownshop/callback.html", context={"status": order.status,'thank':thank,'id':id})
        else:
            order.status = False
            order.save()
            return render(request, "ownshop/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = False
        order.save()
    return render(request, "ownshop/callback.html")
    
    
@login_required(login_url='login')
def tracker(request):
    if request.method == 'GET':
        return render(request,'ownshop/tracker.html')
    elif request.method == 'POST':
        id = request.POST.get('orid')
        order = Order.objects.get(provider_order_id=id)
        order_items = order.items_json
        order_json = json.loads(order_items)
        list_order = list(order_json.keys())
        all_order = []
        for i in list_order:
            my_orders = order_json.get(i)
            all_order.append(my_orders)
        d = {'oid':all_order}
        return render(request,'ownshop/tracker.html',context=d)



def admin_view(request):
    resp = render(request,"ownshop/adminpage.html")
    return resp



def admin_orders_view(request):
    orders = Order.objects.all()
    d = {"orders":orders}
    resp = render(request,"ownshop/adminorders.html",context=d)
    return resp

def admin_contact_view(request):
    contacts = Contact.objects.all()
    d = {"contacts":contacts}
    resp = render(request,"ownshop/admincontacts.html",context=d)
    return resp


def admin_products_view(request):
    products = Product.objects.all()
    d = {"products":products}
    resp = render(request,"ownshop/adminproducts.html",context=d)
    return resp

def admin_users_view(request):
    users = User.objects.all()
    d = {"users":users}
    resp = render(request,"ownshop/adminusers.html",context=d)
    return resp




def add_product_details(request):
    if request.method == "POST":
        products = Product.objects.all()
        d = {"products":products}
        cur_product = Product()
        cur_product.product_name = request.POST.get("productname")
        cur_product.desc1 = request.POST.get("desc1")
        cur_product.desc2 = request.POST.get("desc2")
        cur_product.desc3 = request.POST.get("desc3")
        cur_product.product_catagory = request.POST.get("catagory")
        cur_product.product_sub_catagory = request.POST.get("subcatagory")
        cur_product.product_price = float(request.POST.get("price"))
        cur_product.image = request.FILES['image']
        cur_product.save()
        resp = render(request,"ownshop/adminproducts.html",context=d)
        return resp
    resp = render(request,"ownshop/addproductdetails.html")
    return resp


def edit_product_details(request,myid):
    product = Product.objects.filter(id= myid)
    d = {"product":product}
    if request.method == "POST":
        if "delProduct" in request.POST:
            products = Product.objects.all()
            d1 = {"products":products}
            Product.objects.get(id=myid).delete()
            resp = render(request,"ownshop/adminproducts.html",context=d1)
            return resp
        elif "editProduct" in request.POST:
            cur_product = Product.objects.get(id=myid)
            cur_product.product_name = request.POST.get("productname")
            cur_product.desc1 = request.POST.get("desc1")
            cur_product.desc2 = request.POST.get("desc2")
            cur_product.desc3 = request.POST.get("desc3")
            cur_product.product_catagory = request.POST.get("catagory")
            cur_product.product_sub_catagory = request.POST.get("subcatagory")
            cur_product.product_price = float(request.POST.get("price"))
            cur_product.image = request.FILES['image']
            cur_product.save()
            resp = render(request,"ownshop/editproductdetails.html",context=d)
            return resp
    resp = render(request,"ownshop/editproductdetails.html",context=d)
    return resp




def add_user_details(request):
    if request.method == "POST":
        users = User.objects.all()
        d = {"users":users}
        cur_user = User()
        cur_user.email = request.POST.get("email")
        cur_user.first_name = request.POST.get("fname")
        cur_user.last_name = request.POST.get("lname")
        cur_user.mobile = request.POST.get("mobile")
        cur_user.address = request.POST.get("address")
        cur_user.password = make_password(request.POST.get("password"))
        cur_user.save()
        resp = render(request,"ownshop/adminusers.html",context=d)
        return resp
    resp = render(request,"ownshop/adduserdetails.html")
    return resp


def edit_user_details(request,myid):
    user = User.objects.filter(id= myid)
    d = {"user":user}
    if request.method == "POST":
        if "delUser" in request.POST:
            users = User.objects.all()
            d1 = {"users":users}
            User.objects.get(id=myid).delete()
            resp = render(request,"ownshop/adminusers.html",context=d1)
            return resp
        elif "editUser" in request.POST:
            cur_user = User.objects.get(id=myid)
            cur_user.email = request.POST.get("email")
            cur_user.first_name = request.POST.get("fname")
            cur_user.last_name = request.POST.get("lname")
            cur_user.mobile = request.POST.get("mobile")
            cur_user.address = request.POST.get("address")
            cur_user.password = make_password(request.POST.get("password"))
            cur_user.save()
            resp = render(request,"ownshop/edituserdetails.html",context=d)
            return resp
    resp = render(request,"ownshop/edituserdetails.html",context=d)
    return resp



def add_contact_details(request):
    if request.method == "POST":
        contacts = Contact.objects.all()
        d = {"contacts":contacts}
        cur_contact = Contact()
        cur_contact.name = request.POST.get("name")
        cur_contact.email = request.POST.get("email")
        cur_contact.phone = request.POST.get("phone")
        cur_contact.desc = request.POST.get("desc")
        cur_contact.save()
        resp = render(request,"ownshop/admincontacts.html",context=d)
        return resp
    resp = render(request,"ownshop/addcontactdetails.html")
    return resp




def edit_contact_details(request,myid):
    contact = Contact.objects.filter(msg_id= myid)
    d = {"contact":contact}
    if request.method == "POST":
        if "delContact" in request.POST:
            contacts = Contact.objects.all()
            d1 = {"contacts":contacts}
            Contact.objects.get(msg_id=myid).delete()
            resp = render(request,"ownshop/admincontacts.html",context=d1)
            return resp
        elif "editContact" in request.POST:
            cur_contact = Contact.objects.get(msg_id = myid)
            cur_contact.name = request.POST.get("name")
            cur_contact.email = request.POST.get("email")
            cur_contact.phone = request.POST.get("phone")
            cur_contact.desc = request.POST.get("desc")
            cur_contact.save()
            resp = render(request,"ownshop/editcontactdetails.html",context=d)
            return resp
    resp = render(request,"ownshop/editcontactdetails.html",context=d)
    return resp




def add_order_details(request):
    if request.method == "POST":
        orders = Order.objects.all()
        d = {"orders":orders}
        cur_order = Order()
        cur_order.provider_order_id = request.POST.get("orderid")
        cur_order.payment_id = request.POST.get("paymentid")
        cur_order.signature_id = request.POST.get("signatureid")
        cur_order.status = request.POST.get("status")
        cur_order.items_json = request.POST.get("itemjson")
        cur_order.amount = int(request.POST.get("amount"))
        cur_order.email = request.POST.get("email")
        cur_order.name = request.POST.get("name")
        cur_order.address = request.POST.get("address")
        cur_order.city = request.POST.get("city")
        cur_order.state = request.POST.get("state")
        cur_order.zip_code = request.POST.get("zipcode")
        cur_order.mobile = request.POST.get("mobile")
        
        cur_order.save()
        resp = render(request,"ownshop/adminorders.html",context=d)
        return resp
    resp = render(request,"ownshop/addorderdetails.html")
    return resp



def edit_order_details(request,myid):
    order = Order.objects.filter(id= myid)
    d = {"order":order}
    if request.method == "POST":
        if "delOrder" in request.POST:
            orders = Order.objects.all()
            d1 = {"orders":orders}
            Order.objects.get(id=myid).delete()
            resp = render(request,"ownshop/adminorders.html",context=d1)
            return resp
        elif "editOrder" in request.POST:
            cur_order = Order.objects.get(id = myid)
            cur_order.provider_order_id = request.POST.get("orderid")
            cur_order.payment_id = request.POST.get("paymentid")
            cur_order.signature_id = request.POST.get("signatureid")
            status = request.POST.get("status")
            cur_order.status = True if status == "on" else  False
            cur_order.items_json = request.POST.get("itemjson")
            cur_order.amount = int(request.POST.get("amount"))
            cur_order.email = request.POST.get("email")
            cur_order.name = request.POST.get("name")
            cur_order.address = request.POST.get("address")
            cur_order.city = request.POST.get("city")
            cur_order.state = request.POST.get("state")
            cur_order.zip_code = request.POST.get("zipcode")
            cur_order.mobile = request.POST.get("mobile")
            cur_order.save()
            resp = render(request,"ownshop/editorderdetails.html",context=d)
            return resp
    resp = render(request,"ownshop/editorderdetails.html",context=d)
    return resp
