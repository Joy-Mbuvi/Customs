from rest_framework import serializers
from .models import *


#customer serializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Customers
        fields='__all__'
        extra_kwargs = {
            'phone_number': {'required': True}  
        }

    def validation_phone_number(self,value):
        if len(value) != 10:
            raise serializers.ValidationError('The phone number has to be 10 digits')
        return value


#order serializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['customer','Items','amount','time']
