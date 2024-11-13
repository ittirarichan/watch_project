from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.

def watch_login(req):
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            return redirect(watch_home)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(watch_login)
    else:
        return render(req,'login.html')


def watch_home(req):
    return render(req,'watch/home.html')


def register(req):
    return render(req,'register.html')