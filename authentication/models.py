from django.db import models
from django.contrib.auth.models import AbstractUser

from master.models import AppClient, Customer

class User(AbstractUser):
   app_client = models.ForeignKey(AppClient,on_delete=models.CASCADE,null=True,blank=True)
   customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
   # you can add more fields here.