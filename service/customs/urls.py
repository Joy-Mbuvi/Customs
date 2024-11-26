from django.urls import path
from .views import *



urlpatterns=[
    path('customers/',All_customers.as_view(),name='all customers'),
    path('customers/new/',Create_customers.as_view(),name='Create new consumer'),
    path('orders/<int:customer_id>/',All_order.as_view(),name='Orders'),
    path('orders/new/',Create_orders.as_view(),name='Create new orders'),
    path('accounts/profile/', custom_login_redirect), 
    path('dashboard/', dashboard, name='dashboard'),  

]

