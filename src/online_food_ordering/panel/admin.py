from django.contrib import admin
from .models import User, Restaurant, Guest, Food, Menu
from django import forms

# Register your models here.

class UserForm(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_logedin', 'token']
    readonly_fields = ['id','username', 'email', 'user_type', 'hashed_password', 'salt', 'is_logedin', 'token']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
        # if obj:
        #     return self.readonly_fields + ('id', 'username', 'email', 'user_type', 'hashed_password', 'salt', 'is_logedin', 'token')
        # return self.readonly_fields


class RestaurantForm(admin.ModelAdmin):
    list_display = ['user', 'show_menues', 'show_orders']
    readonly_fields = ['user', 'menus', 'orders']

    def show_menues(self, obj):
        return "\n-".join([m.name for m in obj.menus.all()])

    
    def show_orders(self, obj):
        return "\n-".join([o.user for o in obj.orders.all()])


class GuestForm(admin.ModelAdmin):
    list_display = ['token']


class FoodForm(admin.ModelAdmin):
    list_display = ['foodID','name', 'price', 'availablity']
    readonly_fields = ['name']

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         self.readonly_fields += ('price', 'availablity')
    #     return self.readonly_fields

class MenuForm(admin.ModelAdmin):
    list_display = ['id', 'name', 'rest_token', 'show_foods']

    def show_foods(self, obj):
        return "\n-".join([f.name for f in obj.foods.all()])


admin.site.register(User, UserForm)
admin.site.register(Restaurant, RestaurantForm)
admin.site.register(Guest, GuestForm)
admin.site.register(Food, FoodForm)
admin.site.register(Menu, MenuForm)