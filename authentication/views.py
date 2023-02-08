from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
# Create your views here.
def home(req):
    return render (req, "authentication/index.html")
def signup(request):
    
    if (request.method == "POST"):
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        con_password = request.POST.get("con_password")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")
        elif password != con_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
        else:
            
            myuser = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email, password=password)
            myuser.save()
            messages.success(request, "Account created successfully, login to continue")
            return redirect("login")
        
        
    return render (request, "authentication/signup.html")
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request,user)
            return render(request, "authentication/index.html", {'fname': user.first_name, 'lname': user.last_name})
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
        
    return render (request, "authentication/login.html")
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")