from django.shortcuts import render
from django.utils.crypto import get_random_string, hashlib

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder

from . import models, utils
from .models import User, Restaurant
# Create your views here.


@csrf_exempt
def register_user(request):
    """register a user in system"""

    if 'username' in request.POST.keys():
        this_username = request.POST['username']

    if 'email' in request.POST.keys():
        email = request.POST['email']


    if 'password' in request.POST.keys():
        password = request.POST['password']
        salt = get_random_string(length=16)
        hashed_password = utils.hashPassword(password, salt)

    # define what type is the user
    if 'user_type' in request.POST.keys():
        user_type = int(request.POST['user_type'])
    

    # Duplicate username error: another user already has chosen this username 
    if User.objects.filter(username=this_username).count() != 0:
        return JsonResponse({
            'status': 'Error',
            'message': 'username was already defined'
        }, encoder=DjangoJSONEncoder)


    if User.objects.filter(email=email).count() != 0:
        return JsonResponse({
            'status': 'Error',
            'message': 'Email is used before'
        }, encoder=DjangoJSONEncoder)

    token = get_random_string(length=32)

    new_user = User(username=this_username, 
                    email=email, 
                    salt=salt, 
                    hashed_password=hashed_password, 
                    user_type=user_type, 
                    is_logedin=True, 
                    token = token
                    )
    new_user.save()

    if user_type == 1:
        restaurant = Restaurant(user=new_user)
        restaurant.save()

    return JsonResponse({
        'status' : 'ok',
        'message' : 'User registerd'
    }, encoder=DjangoJSONEncoder)



@csrf_exempt
def login(request):
    """login user"""

    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'username field is empty'
        }, encoder=DjangoJSONEncoder)
    if 'password' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'password field is empty'
        }, encoder=DjangoJSONEncoder)

    if 'user_type' in request.POST.keys() and request.POST['user_type'] != '':
        user_type = request.POST['user_type']
    else:
        user_type = 1

    this_username = request.POST['username']
    this_password = request.POST['password']

    if User.objects.filter(username=this_username).count() == 0:
        return JsonResponse({
            'status': 'Error',
            'message': f'No user with username \"{this_username}\"'
        }, encoder=DjangoJSONEncoder)

    user_obj = User.objects.get(username=this_username)

    if int(user_obj.user_type) != int(user_type):
        return JsonResponse({
            'status': 'Error',
            'message': 'user_type does not match'
        }, encoder=DjangoJSONEncoder)

    if utils.hashPassword(this_password, user_obj.salt) == user_obj.hashed_password:
        user_obj.is_logedin = True
        return JsonResponse({
            'status': 'ok',
            'message': 'user loged in'
        }, encoder=DjangoJSONEncoder)
    else:
        return JsonResponse({
            'status': 'Error',
            'message': 'wrong password'
        }, encoder=DjangoJSONEncoder)
