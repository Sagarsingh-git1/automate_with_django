from django.db import models

# Create your models here.

class Student(models.Model):
    roll_no=models.CharField(max_length=10,unique=True)
    name=models.CharField(max_length=20)
    age=models.IntegerField()


    def __str__(self):
        return self.name
class Customer(models.Model):
    customer_name=models.CharField(max_length=30)
    country=models.CharField(max_length=20)

    def __str__(self):
        return self.customer_name
    
class Employee(models.Model):
    emp_id=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=50)
    designation=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

    