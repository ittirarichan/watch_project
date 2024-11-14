from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


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
        return render(req,'watch/home.html')
    return render(req,'register.html')