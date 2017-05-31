from __future__ import unicode_literals

from django.db import models
import re
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import re, md5
import binascii
from os import urandom
from datetime import date

class UserManager(models.Manager):
    def user_validation(self, postData):
        print postData
        errors = []

        if len(postData['name']) < 3:
            errors.append("Name field cannot be blank and must be at least 3 characters in length.")

        if len(postData['user_name']) < 3:
            errors.append("User name field cannot be blank and must be at least 3 characters in length.")
        try:
            User.objects.get(user_name = postData['user_name'])
            errors.append("User name has already been taken. Please try again.")
        except:
            pass

        if len(postData['password']) < 8:
            errors.append("Password field cannot be blank and must be at least 8 characters in length.")
        if len(postData['confirm']) < 1:
            errors.append("Please confirm your password")
        if not postData["password"] == postData["confirm"]:
            errors.append("Your passwords do not match")
        if len(postData["hire"]) < 1:
            errors.append("Please provide your date of birth.")
        if postData["hire"] > str(date.today()):
			errors.append("That date is in the future and our time-machine is broken... Your DOB by must be today or a past date.")


        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            salt = binascii.b2a_hex(urandom(15))
            hashed_password = md5.new(postData['password']+salt).hexdigest()
            user = self.create(name=postData['name'], user_name=postData['user_name'], password=postData['password'], DOB=postData['hire'], salt=salt)
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def login_validation(self, postData):
        print postData
        login_errors = []

        try:
            User.objects.get(user_name=postData["user_name"])
            print ("$"*20 + "Correct User" + "$"*20)
        except:
            login_errors.append("The user name you entered is inccorect")
        try:
            User.objects.get(user_name=postData["user_name"], password = postData["password"])
            print ('%'*20 + "PASSWORD MATCH")
        except:
            login_errors.append("Password incorrect")

        response_to_views = {}
        if login_errors:
            response_to_views['status'] = False
            response_to_views['errors'] = login_errors
        else:
            user = User.objects.get(user_name=postData["user_name"])
            response_to_views['status'] = True
            response_to_views['user'] = user
        print response_to_views
        return response_to_views

class User(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    DOB = models.DateField()
    salt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
