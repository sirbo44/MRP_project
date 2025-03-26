from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

def to_login(request):
    return redirect('login')

def login(request):
    return render(request, "login.html")

def home(request):
    context = {"page" : "home"}
    return render(request, "home.html", context)

def estimation_period(request):
    context = {"page" : "estimation period"}
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

