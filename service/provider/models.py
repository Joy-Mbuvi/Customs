from django.db import models

class Customers (models.Model):
    name= models.CharField(max_length=100)
    code =models.IntegerField()

class Order(models.Model):
    customer= models.ForeignKey(Customers,on_delete=models.CASCADE)
    Items= models.TextField(max_length=200)
    amount= models.DecimalField(max_digits=10,decimal_places=2)
    time= models.TimeField(auto_now_add=True)


