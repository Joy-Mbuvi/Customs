from django.urls import path
from .views import *



urlpatterns=[
    path('customers/',All_customers.as_view(),name='all customers'),
    path('customers/new/',Create_customers.as_view(),name='Create new consumer'),
    path('customers/google/callback/', GoogleOAuthCallback.as_view(), name='google_oauth_callback'),
    path('orders/<int:customer_id>/',All_order.as_view(),name='Orders'),
    path('orders/new/',Create_orders.as_view(),name='Create new orders'),
    path('dashboard/', dashboard, name='dashboard'),  
    path('create/', create_customer_page, name='create_customer_page'),

]

