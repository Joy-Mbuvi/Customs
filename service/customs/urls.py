from django.urls import path
from .views import *



urlpatterns=[
    path('customers/',All_customers.as_view(),name='all customers'),
    path('customers/new/',New_customer.as_view(),name='Create new consumer'),
    path('orders/<int:customer_id>/',All_order.as_view(),name='Orders'),
    path('auth/google/', views.Google_sign.as_view(), name='google_login'),
    path('auth/jwt/token/', views.Get_Jwt.as_view(), name='get_jwt_token'),
    path('orders/new/',Create_orders.as_view(),name='Create new orders'),
    path('create/', create_customer_page, name='create_customer_page'),

]

