from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import redirect,render
from .models import Customers, Order
from .serializers import CustomerSerializer, OrderSerializer
from django.conf import settings
from django.http import HttpResponseRedirect
import requests
import africastalking

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


             client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
             return redirect(
                    f"https://accounts.google.com/o/oauth2/auth"
                    f"?client_id={client_id}"
                    f"&redirect_uri=http://localhost:8000/customs/customers/google/callback/"
                    f"&response_type=code&scope=openid profile email"
                )

        


        except:   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        # print("Token response status:", response.status_code)

        token_data = response.json()
        # print ('token response data',token_data)
        access_token = token_data['access_token']
        print(f"Access Token: {access_token}")  

        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)

        auhenticated_customer=user_info_response.json()
        name= auhenticated_customer.get('name')


        customer= Customers.objects.get(name=name)

        refresh=RefreshToken.for_user(customer)

        return  Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })




class All_customers(APIView):
    # permission_classes = [IsAuthenticated] 

    def get(self, request):

        
        try:
            data = Customers.objects.all()
            serializer = CustomerSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Unable to fetch customers'}, status=status.HTTP_500_INTERNAL_SERVER_ERROr)


class All_order(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        try:
            orders = Order.objects.filter(customer__id=customer_id)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        


africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
sms = africastalking.SMS
class Create_orders(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            customer_id = request.data.get('customer')
            customer = Customers.objects.get(id=customer_id)
            request.data['customer'] = customer.id  
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()


                message = f"Dear {customer.name}, your order has been placed successfully. Thank you for shopping with us!"
                phone_number = customer.phone_number

                response = sms.send(message, [phone_number])

                if response:
                    return Response({'message': 'Order created and SMS sent successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Order created, but SMS sending failed'}, status=status.HTTP_400_BAD_REQUEST)

        except Customers.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
