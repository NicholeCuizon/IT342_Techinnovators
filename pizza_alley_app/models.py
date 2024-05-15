from django.db import models

# Create your models here.
class Employee(models.Model):
    employeeID = models.CharField(max_length=11, primary_key=True)
    employeeName = models.CharField(max_length=128)
    password = models.CharField(max_length=50)
    role = models.IntegerField()

class Orders(models.Model):
    orderid = models.AutoField(primary_key=True)
    employeeID = models.CharField(max_length=11)
    employeeName = models.CharField(max_length=128)
    totalSales = models.FloatField()
    transactionDate = models.DateField(auto_now_add=True)

class Products(models.Model):
    productID = models.CharField(max_length=5, primary_key=True)
    productName = models.CharField(max_length=200)
    price = models.FloatField()

class Sales(models.Model):
    salesID = models.AutoField(primary_key=True)
    orderID = models.IntegerField()
    productID = models.CharField(max_length=11)
    productName = models.CharField(max_length=128)
    quantity = models.IntegerField()
    total = models.FloatField()

class CurrentOrder(models.Model):
    id = models.AutoField(primary_key=True)
    productID = models.CharField(max_length=5)
    item = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
