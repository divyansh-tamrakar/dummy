from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from matplotlib.style import context
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from .forms import NewUserForm
# Create your views here.

def Userlogin(request):
    page = "login"

    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        if User.objects.get(username=username) is None:
            messages.error(request, "User does not exists!")

        else:
            user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
    context = {'page': page}
    return render(request, 'store/login.html', context)


def signup(request):

    page = "signup"

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            login(request, newuser)
            messages.success(request, "User login successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration.")

    form = NewUserForm()
    context = {'page': page, 'form': form}

    return render(request, 'store/login.html', context)
        
def logoutUser(request):

    logout(request)
    return redirect('home')

def store(request):
    
    data = cartData(request) # cartData function defined in utils.py
    cartItems =  data['number']
    order =  data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'number': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request) # cartData function defined in utils.py
    cartItems =  data['number']
    order =  data['order']
    total =  data['total']
    items =  data['items']
    print(total)
    context = {'items': items, 'total': total, 'order': order, 'number': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request): 
    
    data = cartData(request) # cartData function defined in utils.py

    cartItems =  data['number']
    order =  data['order']
    total =  data['total']
    items =  data['items']
    
    context = {'items': items, 'total': total, 'order': order, 'number': cartItems, 'shipping': False}

    return render(request, 'store/checkout.html', context)


def updateItem(request):

    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    print('productId: ', productId)
    print('Action: ', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer= customer, complete= False)
    
    else:
        
        customer, order = guestOrder(request, data) # guestOrder = funtion defined in utils.py 
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    items = order.orderitem_set.all()
    total_ = 0
    for item in items:
        total_ += item.product.price * item.quantity

    if total == total_:
        order.complete = True
    order.save()

    if order.shipping == True:

        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        ) 

    return JsonResponse('Payment completed!', safe=False)