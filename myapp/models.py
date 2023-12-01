from django.db import models

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    
    def __str__(self):
        return self.name
    
class Register(models.Model):
    fname=models.CharField(max_length=200)
    lname=models.CharField(max_length=200)
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    password=models.CharField(max_length=8)
    image=models.ImageField()
    
    def __str__(self):
        return self.fname
    
