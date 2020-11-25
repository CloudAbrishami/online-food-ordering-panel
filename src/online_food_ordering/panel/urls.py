from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login, name='user login'),
    path('logout/', views.logout, name='user logout'),
    path('enter/', views.enter, name='guest enter'),
    path('exit/', views.exit, name='guest exit')
]
