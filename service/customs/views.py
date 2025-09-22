from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import redirect,render
from .models import Customers, Order
from .serializers import CustomerSerializer, OrderSerializer
from django.conf import settings
import requests
from django.contrib.auth.models import User
from django.db import IntegrityError

from .send_sms import Sendsms

def create_customer_page(request):
    return render(request, 'create_customer.html')


class Google_sign(APIView):
    permission_classes =[AllowAny]

    def get(self,request):
        return redirect('/accounts/google/login/')

class Get_Jwt(APIView):
    permission_classes =[AllowAny]


    def get(self,request):
        if request.user.is_authenticated:
            refresh=RefreshToken.for_user(request.user)
            return Response({
                'access':str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'error': 'Not authenticated'}, status=401)

    
class New_customer(APIView):
    permission_classes =[AllowAny]

    def post(self,request):
        serializer= CustomerSerializer(data=request.data)
        if serializer is_valid():
            customer= serializer.save()
            return Response({'message':'User created successfully',status=201})
        return Response(serializer.errors, status=400)

        

class All_customers(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):

        
        try:
            data = Customers.objects.all()
            serializer = CustomerSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Unable to fetch customers'}, status=status.HTTP_500_INTERNAL_SERVER_ERROr)


class All_order(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        try:
            orders = Order.objects.filter(customer__id=customer_id)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        


class Create_orders(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            customer_id = request.data.get('customer')
            customer = Customers.objects.get(id=customer_id)
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order=serializer.save()


                message = f"Dear {customer.name}, your order #{order.id} has been placed successfully. Thank you for shopping with us!"
                phone_number = customer.phone_number

                sms_sender=Sendsms()
                try:
                 response = sms_sender.send(message, [phone_number])

                 if response:
                    return Response({'message': 'Order created and SMS sent successfully'}, status=status.HTTP_201_CREATED)
                 else:
                       return Response(
                            {'warning': 'Order created, but SMS sending failed'},
                            status=status.HTTP_201_CREATED,
                        )

                except Exception as sms_error:
                    return Response(
                        {
                            'warning': 'Order created successfully, but an error occurred while sending SMS.' ,'sms_error': str(sms_error),
                        },
                        status=status.HTTP_201_CREATED,
                    )

        except Customers.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
