from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
# Create your views here.


def store(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # number = 0
        # for item in items:
            
        #     number += item.quantity
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'number': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    total = 0
    number = 0
    for item in items:
        total += item.product.price * item.quantity
        number += item.quantity
    
    context = {'items': items, 'total': total, 'order': order, 'number': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    
    total = 0
    for item in items:
        total += item.product.price * item.quantity
        

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

    else:
        print("user is not logged in!")

    return JsonResponse('Payment completed!', safe=False)