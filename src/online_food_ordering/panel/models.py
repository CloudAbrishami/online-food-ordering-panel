from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    salt = models.CharField(max_length=128)
    hashed_password = models.CharField(max_length=400)
    phone_number = models.BigIntegerField()
    user_type = models.IntegerField(default=1)  # 1: restaurant | 2: normal users | 3: guest

    def __str__(self):
        return f"{self.username}"

    def __del__(self):
        pass


class Menu(models.Model):
    restaurant = models.ForeignKey(User)
    menu = models.OneToOneField(Food, on_delete=models.CASCADE)


class Food(models.Model):
    foodID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    inventory = models.IntegerField(default=0)

