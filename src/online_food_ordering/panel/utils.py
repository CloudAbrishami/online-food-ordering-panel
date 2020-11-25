from django.utils.crypto import hashlib

def hashPassword(password, salt):
    salted_password = salt + password
    return hashlib.md5(salted_password.encode()).hexdigest()
