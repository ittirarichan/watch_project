from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.




def watch_login(req):
    if 'shop' in req.session:
        return redirect(watch_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        # print('jgfdt')
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=username
                return redirect(watch_home)
            else:
                req.session['user']=username
                return redirect(user_home)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(watch_login)
    else:
        return render(req,'login.html')

def watch_shop_logout(req):
    logout(req)
    req.session.flush()                   #session delete
    return redirect(watch_login)



#--------------------admin------------------------

def watch_home(req):
    if 'shop' in req.session:              #checking section status
        data=Product.objects.all()
        return render(req,'watch/home.html',{'products':data})
    else:
        return redirect(watch_login)



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
    


def edit_product(req,pid):
    if req.method=='POST':
        product_id=req.POST['product_id']
        name=req.POST['name']
        description=req.POST['description']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        file=req.FILES.get('img')
        if file :
            Product.objects.filter(pk=product_id).update(pid=product_id,name=name,dis=description,
                                            price=price,offer_price=offer_price,stock=stock,img=file)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()

        else:
            Product.objects.filter(pk=pid).update(pid=product_id,name=name,dis=description,
                                            price=price,offer_price=offer_price,stock=stock)
            return redirect(watch_home)
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'watch/edit_product.html',{'data':data})
    
def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/' + file)
    data.delete()
    return redirect(watch_home)




#--------------------user------------------------

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        pswd=req.POST['password']
        send_mail("Account created","succesfully completed", settings.EMAIL_HOST_USER, [email])

        try:
            data=User.objects.create_user(first_name=name,email=email,username=email,password=pswd)    

            data.save()
        except:
            messages.warning(req, "Username/email already exist.")
            return redirect(register)
        return redirect(watch_login)
    else:
        return render(req,'user/register.html')
    
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render (req,'user/user_home.html',{'products':data})
    else:
        return redirect(watch_login)
    
def view_product(req,pid):
    data=Product.objects.get(pk=pid)
    return render(req,'user/view_product.html',{'product':data})

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})  

def qty_inc(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()  
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()  
    if data.qty==0:
        data.delete()
    return redirect(view_cart)

def remove_cart(req,cid):
    data=Cart.objects.get(pk=cid)

    data.delete()
    return redirect(view_cart)

def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'bookings':buy})


  
def contact(req):
    return render(req,'user/contact.html')   
def booking(req):
    return render(req,'user/booking.html')   
def about(req):
    return render(req,'user/about.html')   



