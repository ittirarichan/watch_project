from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *


# Create your views here.

def watch_login(req):
    if 'shop' in req.session:
        return redirect(watch_home)
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            req.session['shop']=username #session create
            return redirect(watch_home)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(watch_login)
    else:
        return render(req,'login.html')

def watch_shop_logout(req):
    logout(req)
    req.session.flush()                   #session delete
    return redirect(watch_login)


def watch_home(req):
    if 'shop' in req.session:              #checking section status
        data=Product.objects.all()
        return render(req,'watch/home.html',{'products':data})
    return render(req,'register.html')


def register(req):
    return render(req,'register.html')

def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            product_id=req.POST['product_id']
            name=req.POST['name']
            description=req.POST['description']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            stock=req.POST['stock']
            file=req.FILES['image']
            data=Product.objects.create(pid=product_id,name=name,dis=description,
                                         price=price,offer_price=offer_price,stock=stock,img=file)
            data.save()
            return redirect(watch_home)
        else:
            return render(req,'watch/add_product.html')
    else:
        return redirect(watch_login)