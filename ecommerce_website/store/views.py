from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    else:
        items = []
    total = 0
    number = 0
    for item in items:
        total += item.product.price * item.quantity
        number += item.quantity

    context = {'items': items, 'total': total, 'number': number}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    else:
        items = []
    total = 0
    number = 0
    for item in items:
        total += item.product.price * item.quantity
        number += item.quantity

    context = {'items': items, 'total': total, 'number': number}

    return render(request, 'store/checkout.html', context)


def updateItem(request):
    return JsonResponse('Item was added', safe=False)
