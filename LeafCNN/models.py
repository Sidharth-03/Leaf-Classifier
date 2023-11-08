from django.db import models
from django import forms

# Create your models here.
class Contact(models.Model):
     name=models.CharField(max_length=120)
     email=models.EmailField(max_length=120)
     message=models.TextField()
     datetime=models.DateTimeField()
    
