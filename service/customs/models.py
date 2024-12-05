from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=False, unique=True, null=True)  
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True,validators=[
            RegexValidator(
                 regex=r'^\+254\d{9}$',  
                message="Phone number must be entered in the format: '+254' followed by 9 digits."
            )])  
            

   


    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    Items = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField(auto_now_add=True)


