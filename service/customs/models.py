from django.db import models

class Customers (models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(blank=False,null=True,unique=True)
    code=models.IntegerField( default=33227)
    phone_number=models.CharField(max_length=15, unique=True, blank=True, null=True)

class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    Items = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField(auto_now_add=True)


