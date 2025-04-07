from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import User



def to_login(request):
    return redirect('login')

def login(request):
    # on POST requests
    if request.method == 'POST':
        # get the username and the password from the user
        username = request.POST.get("username")
        password = request.POST.get("password")
        # get all the user records from the server
        users = User.objects.all().values()
        # check the username's validity 
        for user in users:
            # if username is correct
            if user['username'] == username:
                # if password is correct
                if user['password'] == password:
                    # send user to the correct homepage
                    # if user['role'] == 'user':            LATER WHEN ADD ADMIN PAGE   
                    return redirect('home')
        else:
            # return error message and render to login
            return render(request, "login.html", {'message':'Wrong credentials! Please try again'})
    return render(request, "login.html")

def home(request):
    context = {"page" : "home"}
    return render(request, "home.html", context)

def estimation_period(request):
    context = {"page" : "estimation period",
               "range": range(3)}
    return render(request, "estimation_period.html", context)

def track_order(request):
    context = {"page" : "track order"}
    return render(request, "track_order.html", context)

def archive(request):
    context = {"page" : "archive"}
    return render(request, "archive.html", context)

def forecasting(request):
    context = {"page" : "forecasting"}
    return render(request, "forecasting.html", context)

def report(request):
    context = {"page" : "report"}
    return render(request, "report.html", context)

