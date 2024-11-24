from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from models import *
from serializers import *

# Create your views here.
#view for getting all your customers

class All_customers(APIView):
    def get (self,request):
        try:
         data=  Customers.objects.all()
         serializer=CustomerSerializer(data,many=True)
         return Response(serializer.data,status=status.HTTP_200_OK)
        except:
           return Response('error', status=status.HTTP_404_NOT_FOUND)
        
#view for cretating a customer

class Create_customers(APIView):
   def post (self,request):
      try:
         serializer= CustomerSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
         return Response({'message':'Customer created sucessfully'},status=status.HTTP_201_CREATED)
      
      except:
         return Response({'error':'Missing credentials'},status=status.HTTP_400_BAD_REQUEST) 


#for orders
class All_order(APIView):
    def get (self,request,customer_id):
        try:
         customer=  Order.objects.get(id=customer_id)
         orders= Order.objects.filter(customer=customer)
         serializer=OrderSerializer(orders,many=True)
         return Response(serializer.data,status=status.HTTP_200_OK)
        except customer.DoesNotExist:
           return Response('Customer Does not exist', status=status.HTTP_404_NOT_FOUND)
        
#view for cretating a customer

class Create_orders(APIView):
   def post (self,request):
      try:
         customer_id= request.data.get ('customer')
         customer= Customers.objects.get(id=customer_id)#makke sure the customer is actually in the 
         request.data['customer']= customer
         serializer= OrderSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
         return Response({'message':'Order created sucessfully'},status=status.HTTP_201_CREATED)
      
      except:
         return Response({'error':'Missing details'},status=status.HTTP_400_BAD_REQUEST) 

