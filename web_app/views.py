from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from .models import User, Order, Customer, Archive
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



# --------------------------REDIRECT TO LOGIN ----------------------------------------------------

def to_login(request):                                                                                  # DONE
    return redirect('login')

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('unauthorized')  # your error page view name
        return view_func(request, *args, **kwargs)
    return wrapper

def custom_login_view(request):                                                                         # DONE
    form = AuthenticationForm(request, data=request.POST or None)
    show_errors = False

    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # replace 'home' with your actual home page route name
        else:
            show_errors = True  # only show errors if login attempt failed

    return render(request, 'registration/login.html', {'form': form, 'show_errors': show_errors})

# ---------------------------HOME PAGE ---------------------------------------------------
@custom_login_required
def home(request):  
    customers = list(Customer.objects.values_list('tin', flat=True))
    orders = Order.objects.all()
    orderCustomers = list(Order.objects.values_list('customer', flat=True))
    shared = set(customers) & set(orderCustomers)

    context = {"page" : "home", "orders": list(orders), 'data':[int(len(customers)-len(shared)), int(len(shared))]}
    return render(request, "home.html", context)

# ----------------------------ESTIMATION PAGES --------------------------------------------------
@custom_login_required
def estimation_period(request):                                                                         # DONE
    context = {"page" : "estimation period"}
    return render(request, "estimation_period.html", context)

@custom_login_required
def estimate(request):                                                                                  # DONE
    numbers = request.GET.getlist('input')
    values = ''
    for number in numbers:
        values+=number+','
    return redirect('estimation_schedule/?data=['+values+']')

path = ''
@custom_login_required
def estimation_schedule(request):                                                                       # DONE
    if request.method == 'GET':
        global path
        data = request.GET.get('data', [])
        data = data[1:-1]
        data = data.split(',')
        data = data[:-1]
        context = {"page" : "estimation schedule", "data":data, 'range' :range(len(data)+1)}
        path = request.get_full_path()
        return render(request, "estimation_schedule.html", context)
    if request.method == 'POST':
        params = path[path.find("=")+1:]
        params = params[:-2]+params[-1]

        if 'phone' in request.POST:
            new_customer = Customer(brand=request.POST['brand'], tin=request.POST['tin'], phone=request.POST['phone'])
            new_customer.save()
        new_order = Order(customer=request.POST['tin'],date=request.POST['date'],schedule=params)   
        new_order.save()
    return redirect('estimation_period')
      

# -------------------------------TRACK ORDERS PAGES -----------------------------------------------
@custom_login_required
def track_order(request):                                                                               # DONE
    orders = Order.objects.all().values()
    context = {"page" : "track order", 'orders':orders}
    return render(request, "track_order.html", context)

@custom_login_required
def monitor(request):                                                                                   # DONE
    orderID = request.GET.get('order')
    order = Order.objects.filter(id = orderID).values()[0]
    data = order['schedule']
    data = data[1:-1]
    data = data.split(',')
    context = {"page": "monitor", "data": data, 'range': range(len(data)+1), 'order':order}
    return render(request, "monitor.html", context)

@custom_login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

# --------------------------------ARCHIVE PAGES ----------------------------------------------
@custom_login_required
def archive(request):                                                                                   # DONE
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

@custom_login_required
def schedule(request):                                                                                  # DONE
    orderID = request.GET.get('order')
    order = Archive.objects.filter(id = orderID).values()[0]
    data = order['schedule']
    data = data[1:-1]
    data = data.split(',')        
    print(order)                                                                        
    context = {"page": "schedule", "data": data, 'range': range(len(data)+1), 'order':order}
    return render(request, "schedule.html", context)

# ---------------------------------FORECASTING PAGES ---------------------------------------------
@custom_login_required
def linear_regression(request):                                                                         # DONE
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

@custom_login_required
def exponential_smoothing(request):                                                                     # DONE
    orders = Archive.objects.all()
    date_val = {}
    for i in range(len(orders)):
        if (str(orders[i].date).split('-')[1] in date_val):
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] += int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
        else:
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] = int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
    print(date_val)
    context = {"page" : "forecasting", "orders": orders, 'data':date_val}
    return render(request, "exponential_smoothing.html", context)

@custom_login_required
def moving_average(request):                                                                            # DONE
    # We get all the archived records from the database in order to perform predictions
    orders = Archive.objects.all()
    date_val = {}
    for i in range(len(orders)):
        if (str(orders[i].date).split('-')[1] in date_val):
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] += int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
        else:
            date_val[str(orders[i].date).split('-')[0]+'-'+str(orders[i].date).split('-')[1]] = int(sum(list(map(int,orders[i].schedule[1:-1].split(',')))))
    print(date_val)
    context = {"page" : "forecasting", "orders": orders, 'data':date_val}
    return render(request, "moving_average.html", context)

# ----------------------------------REPORT PAGES --------------------------------------------
@custom_login_required
def report(request): 
    customers = Customer.objects.all().values()
    orders = Order.objects.all().values()
    archive = Archive.objects.all().values() 
    orders_forecast = Archive.objects.all()
    date_val = {}
    for i in range(len(orders_forecast)):
        if (str(orders_forecast[i].date).split('-')[1] in date_val):
            date_val[str(orders_forecast[i].date).split('-')[0]+'-'+str(orders_forecast[i].date).split('-')[1]] += int(sum(list(map(int,orders_forecast[i].schedule[1:-1].split(',')))))
        else:
            date_val[str(orders_forecast[i].date).split('-')[0]+'-'+str(orders_forecast[i].date).split('-')[1]] = int(sum(list(map(int,orders_forecast[i].schedule[1:-1].split(',')))))   
    context = {"page" : "report", "customers": list(customers), "orders": list(orders), "archive": list(archive), "orders_forecast":orders_forecast, "data":date_val}
    return render(request, "report.html", context)

# ----------------------------------CUSTOMERS --------------------------------------------
@custom_login_required
def customers(request):                                                                                 # DONE
    customers = Customer.objects.all()
    context = {"page": "customers", "customers":customers}
    return render(request, "customers.html", context)

@custom_login_required
def edit(request):                                                                                      # DONE
    tin = request.GET.get('tin')
    customer = Customer.objects.get(tin=tin)
    if request.method == 'POST':
        customer.brand = request.POST.get('brand')
        customer.phone = request.POST.get('phone')
        customer.save()
        return redirect('customers')
    context = {"page":"edit page", "customer":customer}
    return render(request, "edit.html", context)

# ----------------------------------UNAUTHORIZED --------------------------------------------
def unauthorized_view(request):
    return render(request, 'unauthorized.html')

