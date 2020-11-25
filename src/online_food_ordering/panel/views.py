from django.shortcuts import render
from django.utils.crypto import get_random_string, hashlib

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder

from . import models, utils
from .models import User, Restaurant, Guest
# Create your views here.


@csrf_exempt
def register_user(request):
    """register a user in system"""

    if 'username' in request.POST.keys():
        this_username = request.POST['username']
    else:
        return JsonResponse({
        'status' : 'Error',
        'message' : 'username did not specified'
    }, encoder=DjangoJSONEncoder)


    if 'email' in request.POST.keys():
        email = request.POST['email']
    else:
        return JsonResponse({
        'status' : 'Error',
        'message' : 'email did not specified'
    }, encoder=DjangoJSONEncoder)



    if 'password' in request.POST.keys():
        password = request.POST['password']
        salt = get_random_string(length=16)
        hashed_password = utils.hashPassword(password, salt)
    else:
        return JsonResponse({
        'status' : 'Error',
        'message' : 'password did not specified'
    }, encoder=DjangoJSONEncoder)


    # define what type is the user
    if 'type' in request.POST.keys():
        user_type = int(request.POST['type'])
    else:
        return JsonResponse({
        'status' : 'Error',
        'message' : 'User type did not specified'
    }, encoder=DjangoJSONEncoder)

    

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

    if 'type' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'user type field is empty'
        }, encoder=DjangoJSONEncoder)


    this_username = request.POST['username']
    this_password = request.POST['password']
    user_type     = request.POST['type']

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


@csrf_exempt
def logout(request):
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'user did not specified'
        }, encoder=DjangoJSONEncoder)
    
    user_obj = User.objects.get(username=request.POST['username'])
    user_obj.is_logedin = False
    user_obj.save()

    return JsonResponse({
        'status': 'OK',
        'message': 'user loged out'
    }, encoder=DjangoJSONEncoder)



@csrf_exempt
def enter(request):
    token = get_random_string(length=32)

    while User.objects.filter(token=token).count() != 0 and Guest.objects.filter(token=token).count() != 0:
        token = get_random_string(length=32)

    guest = Guest(token=token)
    guest.save()

    return JsonResponse({
        'status': 'OK',
        'message': f"""this user entered successfully as a guest - token: {token}"""
    }, encoder=DjangoJSONEncoder)



@csrf_exempt
def exit(request):
    if 'token' not in request.POST.keys():
        return JsonResponse({
        'status': 'Error',
        'message': 'guest not specified'
    }, encoder=DjangoJSONEncoder)
    
    token = request.POST['token']

    geust_obj = Guest.objects.get(token=token)
    geust_obj.delete()

    return JsonResponse({
        'status': 'OK',
        'message': 'guest successfully exited from the app'
    }, encoder=DjangoJSONEncoder)