from email import message
from urllib import response
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
           # Check username
           if User.objects.filter(username = username).exists():
                messages.error(request,'That username is taken')
                return redirect('register')
           else:
            if User.objects.filter(email = email).exists():
                messages.error(request,'That email is taken')
                return redirect('register')
            else:
                #looks good
                user =  User.objects.create_user(username = username, password=password,email=email, 
                first_name=first_name, last_name = last_name)
                #login after register
                #auth.login(request,user)
                #messages.success(request,"you are not logged in")
                
                user.save()
                messages.success(request,"You are now registered and can login")
                return redirect('login')
                
        else:
            messages.error(request,'Password do not match')
            return redirect('register')

    else:
        return render (request,"accounts/register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"you are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')

    else:
        return render (request,"accounts/login.html")

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'you logged out successfully')
        return HttpResponseRedirect(reverse('index'))
   

def dashboard(request):
    return render(request,"accounts/dashboard.html")