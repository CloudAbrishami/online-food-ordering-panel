from django.db import models
from django.utils.crypto import get_random_string
# Create your models here.

class User(models.Model):
    id               =  models.AutoField(primary_key=True)
    username         =  models.CharField(max_length=255, default=None)   # make sure that no other user is available with the same username
    email            =  models.EmailField(default=None)
    salt             =  models.CharField(max_length=128, default=None)
    hashed_password  =  models.CharField(max_length=400, default=None)
    phone_number     =  models.BigIntegerField(default=None)
    user_type        =  models.IntegerField(default=0)  # 0: guest | 1: restaurant | 2: normal users |
    token            =  models.CharField(max_length=32)
    is_logedin       =  models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        self.token = get_random_string(length=32)

        if self.user_type == 1:
            self.restaurant = Restaurant(user=self)

    def __str__(self):
        if self.username != None:
            return self.username
        else:
            return self.token



class Food(models.Model):
    foodID      =   models.AutoField(primary_key=True)
    name        =   models.CharField(max_length=255)
    price       =   models.FloatField(default=0)
    availablity =   models.IntegerField(default=0)

    def __str__(self):
        return self.name
  

class Order(models.Model):
    foods       = models.ManyToManyField(Food)
    total_price = models.FloatField(default=None)

    def calcute_price(self):
        pass



class Restaurant(models.Model):
    user    =   models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    menus   =   models.ManyToManyField(Food)
    orders  =   models.ManyToManyField(Order, blank=True)