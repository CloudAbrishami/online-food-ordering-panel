from django.contrib import admin
from .models import User, Restaurant
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

admin.site.register(User, UserForm)
admin.site.register(Restaurant, RestaurantForm)
