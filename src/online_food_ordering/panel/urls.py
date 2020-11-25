from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login, name='user login'),
    path('logout/', views.logout, name='user logout'),
    path('enter/', views.enter, name='guest enter'),
    path('exit/', views.exit, name='guest exit'),
    path('restaurant/', views.get_restaurants, name='get restaurants'),
    path('restaurant/menu/', views.get_menu, name='get restaurants'),
    path('restaurant/close/', views.close_restaurant, name='close restaurant'),
    path('restaurant/open/', views.open_restaurant, name='open restaurant'),
    path('restaurant/status/', views.restaurant_status, name='restaurant status'),
    path('food/add/', views.add_food, name="add new food"),
    path('menu/add/', views.add_menu, name='add new menu'),
    path('menu/add/food/', views.add_to_menu, name='add food to menu'),

]
