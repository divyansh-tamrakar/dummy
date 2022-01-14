from django.urls import path
from . import views

# urls

urlpatterns = [
    path('', views.store, name='home'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name="process_order"),
]