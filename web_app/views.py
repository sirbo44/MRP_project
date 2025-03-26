from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

def to_login(request):
    return redirect('login')

def login(request):
    template = loader.get_template("login.html")
    return render(request, "login.html")

