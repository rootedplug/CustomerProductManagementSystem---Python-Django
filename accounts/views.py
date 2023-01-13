from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.cache import cache_control
from .decorators import unauthenticated_user, allowed_user,admin_only

# Create your views here.
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@admin_only
def dashboard(request):
    context = {
        'orders':Orders.objects.all(),
        'customers':Customer.objects.all(),
        'total_orders':Orders.objects.count(),
        'delivered':Orders.objects.filter(status='Delivered').count(),
        'pending':Orders.objects.filter(status='Pending').count()

    }
    return render(request, 'accounts/dashboard.html', context)
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@admin_only
def products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'accounts/products.html', context)
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request, pk_test):
    single_customer = Customer.objects.get(id=pk_test)
    orders = single_customer.orders_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer':single_customer,
        'Orders': orders,
        'Total_orders': single_customer.orders_set.all().count(),
        'filter':myFilter,        
    }
    return render(request, 'accounts/customers.html', context)
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm()
    if request.method == 'POST':
        #print('Printing Post:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
        'customer': customer
    }
    return render(request, 'accounts/order_form.html', context)
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Orders.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    context = {'form':form}
    return render(request,  'accounts/order_form.html', context)
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Orders.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
@unauthenticated_user
def Register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)
@unauthenticated_user
def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/login.html')
def Logout(request):
    logout(request)
    return redirect('login')
@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@allowed_user(allowed_roles=['customers'])
def UserPage(request):
    orders = request.user.customer.orders_set.all()
    context = {'orders':orders}
    return render(request, 'accounts/users.html', context)

@cache_control(no_cache=True, must_validate=True, no_store=True)
@login_required(login_url='login')
@allowed_user(allowed_roles=['customers'])
def AccountSetting(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context = {'form':form}
    return render(request, 'accounts/account_setting.html', context)
