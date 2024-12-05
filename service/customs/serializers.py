from rest_framework import serializers
from .models import *


#customer serializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Customers
        fields='__all__'
        

        
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['customer','Items','amount','time']
