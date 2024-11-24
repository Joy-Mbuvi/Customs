from rest_framework import serializers
from .models import *


#customer serializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields=['__all__']

#order serializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields=['customer','items','amount','time']
