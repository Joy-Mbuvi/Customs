from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import redirect,render
from .models import Customers, Order
from .serializers import CustomerSerializer, OrderSerializer
from django.conf import settings
import africastalking

def dashboard(request):
    return render(request, 'dashboard.html')


def custom_login_redirect(request):
    if request.user.is_authenticated:
        return redirect('/customers/')  # Redirect to customers view

class All_customers(APIView):
    permission_classes = [IsAuthenticated]
    required_scopes = ['read'] 

    def get(self, request):
        try:
            data = Customers.objects.all()
            serializer = CustomerSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except :
            return Response({'error': 'Unable to fetch customers'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Create_customers(APIView):
    permission_classes = [AllowAny]
    required_scopes = ['write']

    def post(self, request):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Customer created successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception :
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class All_order(APIView):
    permission_classes = [IsAuthenticated]
    required_scopes = ['read']

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
    required_scopes = ['read', 'write']

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
