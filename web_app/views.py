from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from .models import User, Order, Customer, Archive
import json


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

path = ''

def estimation_schedule(request):
    if request.method == 'GET':
        # access global variable path
        global path
        # get the values from the URL
        data = request.GET.get('data', [])
        # remove '[', ']' and the last ',' from the data retrieved from the URL
        data = data[1:-1]
        # convert the data to a list 
        data = data.split(',')
        # remove the last empty item
        data = data[:-1]
        context = {"page" : "estimation schedule", "data":data, 'range' :range(len(data)+1)}
        # modify the global variable path
        path = request.get_full_path()
        return render(request, "estimation_schedule.html", context)
    if request.method == 'POST':
        # get the parameters from the url
        params = path[path.find("=")+1:]
        # delete the last ','
        params = params[:-2]+params[-1]

        # in case of new customer 
        if 'phone' in request.POST:
            # create a customer in the database
            new_customer = Customer(brand=request.POST['brand'], tin=request.POST['tin'], phone=request.POST['phone'])
            new_customer.save()
        # create the order for
        new_order = Order(customer=request.POST['tin'],date=request.POST['date'],schedule=params)   
        new_order.save()
    return redirect('estimation_period')
      

# -------------------------------TRACK ORDERS PAGES -----------------------------------------------
def track_order(request):
    orders = Order.objects.all().values()
    context = {"page" : "track order", 'orders':orders}
    return render(request, "track_order.html", context)


def monitor(request):
    orderID = request.GET.get('order')
    order = Order.objects.filter(id = orderID).values()[0]
    data = order['schedule']
    data = data[1:-1]
    data = data.split(',')
    context = {"page": "monitor", "data": data, 'range': range(len(data)+1), 'order':order}
    return render(request, "monitor.html", context)


# --------------------------------ARCHIVE PAGES ----------------------------------------------

def archive(request):
    if request.method == 'POST':
        orderid = int(request.POST.get('order'))
        oldOrder = Order.objects.filter(id = orderid).values()[0]
        newOrder = Archive(id=oldOrder['id'], customer=oldOrder['customer'], date=oldOrder['date'], schedule=oldOrder['schedule'])
        newOrder.save()
        oldOrder = Order.objects.get(id=orderid).delete()
        return redirect('track_order')
    if request.method == 'GET':
        orders = Archive.objects.all()
        context = {"page" : "archive", 'orders':orders}
        return render(request, "archive.html", context)

def schedule(request):
    context = {"page": "schedule"}
    return render(request, "schedule.html", context)

# ---------------------------------FORECASTING PAGES ---------------------------------------------

def linear_regression(request):
    orders = Archive.objects.all()
    date_val = {}
    for i in range(len(orders)):
        if (str(orders[i].date).split('-')[1] in date_val):
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] += int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
        else:
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] = int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
    print(date_val)
    context = {"page" : "forecasting", "orders": orders, 'data':date_val}
    return render(request, "linear_regression.html", context)


def exponential_smoothing(request):
    orders = Archive.objects.all()
    date_val = {}
    for i in range(len(orders)):
        if (str(orders[i].date).split('-')[1] in date_val):
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] += int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
        else:
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] = int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
    print(date_val)
    context = {"page" : "exponential smoothing", "orders": orders, 'data':date_val}
    return render(request, "exponential_smoothing.html", context)


def moving_average(request):
    # We get all the archived records from the database in order to perform predictions
    orders = Archive.objects.all()
    date_val = {}
    for i in range(len(orders)):
        if (str(orders[i].date).split('-')[1] in date_val):
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] += int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
        else:
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] = int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
    print(date_val)
    context = {"page" : "moving average", "orders": orders, 'data':date_val}
    return render(request, "moving_average.html", context)

# ----------------------------------REPORT PAGES --------------------------------------------
def report(request):
    context = {"page" : "report"}
    return render(request, "report.html", context)

# ----------------------------------CUSTOMERS --------------------------------------------
def customers(request):
    customers = Customer.objects.all()
    context = {"page": "customers", "customers":customers}
    return render(request, "customers.html", context)

def edit(request):
    tin = request.GET.get('tin')
    customer = Customer.objects.get(tin=tin)
    if request.method == 'POST':
        customer.brand = request.POST.get('brand')
        customer.phone = request.POST.get('phone')
        customer.save()
        return redirect('customers')
    context = {"page":"edit page", "customer":customer}
    return render(request, "edit.html", context)