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

def dashboard(request):
    return render(request, 'dashboard.html')

def create_customer_page(request):
    return render(request, 'create_customer.html')

class Create_customers(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                # Now return a Response to indicate success
                client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
                redirect_url = f"https://accounts.google.com/o/oauth2/auth" \
                               f"?client_id={client_id}" \
                               f"&redirect_uri=http://localhost:8000/customs/customers/google/callback/" \
                               f"&response_type=code&scope=openid profile email"
                
                return redirect(redirect_url)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GoogleOAuthCallback(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
            'client_secret': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret'],
            'redirect_uri': settings.LOGIN_REDIRECT_URL,
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=data)
        token_data = response.json()

        access_token = token_data.get('access_token')
        if not access_token:
            return Response(
                {'error': 'Failed to obtain access token', 'details': token_data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_info_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}"
        token_info_response = requests.get(token_info_url)
        email = token_info_response.json().get('email')

        # Try to get the user or create if they don't exist
        try:
            user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                # Create a Customers instance if it's a new user
                Customers.objects.create(user=user, email=email)

        except IntegrityError:
            # Handle the case where email already exists
            user = User.objects.get(email=email)
            # Optionally, update other fields of the customer if needed
            customer, _ = Customers.objects.get_or_create(user=user)

        refresh = RefreshToken.for_user(user)
        jwt_access_token = str(refresh.access_token)

        return Response({'jwt_access_token': jwt_access_token}, status=status.HTTP_200_OK)


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
