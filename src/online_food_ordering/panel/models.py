from django.db import models
from django.utils.crypto import get_random_string
# Create your models here.

class User(models.Model):
    id               =  models.AutoField(primary_key=True)
    username         =  models.CharField(max_length=255, default=None, blank=True)   # make sure that no other user is available with the same username
    email            =  models.EmailField(default=None, blank=True)
    salt             =  models.CharField(max_length=128, default=None, blank=True)
    hashed_password  =  models.CharField(max_length=400, default=None, blank=True)
    # phone_number     =  models.BigIntegerField(blank=True)
    user_type        =  models.IntegerField(default=0)  # 1: restaurant | 2: normal
    token            =  models.CharField(max_length=32, blank=True)
    is_logedin       =  models.BooleanField(default=False)


    def __str__(self):
        if self.username != None:
            return self.username
        else:
            return self.token

class Guest(models.Model):
    token = models.CharField(
                        max_length=32,
                        unique=True
    )   


class Food(models.Model):
    foodID      =   models.AutoField(primary_key=True)
    name        =   models.CharField(max_length=255)
    price       =   models.FloatField(default=0)
    availablity =   models.IntegerField(default=0)

    def __str__(self):
        return self.name
  
class Menu(models.Model):
    id      =   models.AutoField(primary_key=True)
    name    =   models.CharField(max_length=100)
    foods   =   models.ManyToManyField(Food, default=None)
    rest_token  = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.name

class Order(models.Model):
    foods       = models.ManyToManyField(Food)
    total_price = models.FloatField(default=None)

    def calcute_price(self):
        pass



class Restaurant(models.Model):
    user    =   models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    menus   =   models.ManyToManyField(Food, blank=True, default=None)
    orders  =   models.ManyToManyField(Order, blank=True)
    token   =   models.CharField(max_length=32, blank=True)