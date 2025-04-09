from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from .models import User, Order, Customer


# --------------------------REDIRECT TO LOGIN ----------------------------------------------------

def to_login(request):                                                                                  # DONE
    return redirect('login')

# ---------------------------LOGIN PAGE ---------------------------------------------------
def login(request):                                                                                     # DONE 
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

# ---------------------------HOME PAGE ---------------------------------------------------
def home(request):                                                                                      # DONE
    context = {"page" : "home"}
    return render(request, "home.html", context)

# ----------------------------ESTIMATION PAGES --------------------------------------------------
def estimation_period(request):                                                                         # DONE
    context = {"page" : "estimation period"}
    return render(request, "estimation_period.html", context)

def estimate(request):                                                                                  # DONE
    # on POST request
    numbers = request.GET.getlist('input')
    # create a string of the values to pass in the URL 
    values = ''
    for number in numbers:
        values+=number+','
    # pass the values in the URL
    return redirect('estimation_schedule/?data=['+values+']')

def estimation_schedule(request):
    # get the values from the URL
    data = request.GET.get('data', [])
    # remove '[', ']' and the last ',' from the data retrieved from the URL
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data[:-1]
    # convert the data to a list 
    data = data.split(',')
    print(data)
    context = {"page" : "estimation schedule", "data":data, 'range' :range(len(data)+1)}
    return render(request, "estimation_schedule.html", context)

def add_order(request):
    if request.method == 'POST':
        # in case of new customer 
        # print(request.POST)                   TO BE DELETED
        if 'phone' in request.POST:
            # create a customer in the database
            new_customer = Customer(brand=request.POST['brand'], tin=request.POST['tin'], phone=request.POST['phone'])
            new_customer.save()
        # create the order for
        new_order = Order(customer=request.POST['tin'],date=request.POST['date'],schedule='test')
        new_order.save()
    return redirect('estimation_period')

# -------------------------------TRACK ORDERS PAGES -----------------------------------------------
def track_order(request):
    context = {"page" : "track order"}
    return render(request, "track_order.html", context)

# --------------------------------ARCHIVE PAGES ----------------------------------------------
def archive(request):
    context = {"page" : "archive"}
    return render(request, "archive.html", context)

# ---------------------------------FIRECASTING PAGES ---------------------------------------------
def forecasting(request):
    context = {"page" : "forecasting"}
    return render(request, "forecasting.html", context)

# ----------------------------------REPORT PAGES --------------------------------------------
def report(request):
    context = {"page" : "report"}
    return render(request, "report.html", context)

# ------------------------------------------------------------------------------
