from email.policy import default
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['firstname']) < 2:
            errors["firstname"] = "User firstname should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "User lastname should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "User password should be at least 8 characters"
        if postData['confirm_password'] != postData['password']:
            errors['confirm_password']="password not match"
        return errors

class User(models.Model):
    firstname = models.CharField(max_length=45)
    lastname=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    email=models.EmailField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()


class Product(models.Model) : 
    product_id = models.IntegerField()
    product_name = models.TextField(max_length=255)
    item_condition_id = models.IntegerField()
    category = models.TextField(max_length=500)
    shipping = models.IntegerField()
    price = models.FloatField(max_length=9)
    item_description = models.TextField(max_length=500)
