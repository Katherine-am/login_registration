from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re
import bcrypt
from django.shortcuts import redirect

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        
        DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}')
        if not DATE_REGEX.match(postData['birthday']):
            errors['invalid'] = "Nice try, Cody."
        else:
            given = datetime.strptime(postData['birthday'], '%Y-%m-%d')
            today = datetime.today()
            if given > today:
                errors['past_birthday'] = 'Birthday must be a date in the past'
            def calculate_age(born):
                today = date.today()
                return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            if calculate_age(given) < 13:
                errors['too young'] = "Please enter a valid birthday. You must be at least 13 years old to access this site."

        #email validation check
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"

        if User.objects.filter(email=postData['email']):
            errors["email"] = "User already exists"

        if len(postData['password']) < 6:
            errors["password"] = "Password must contain more than 6 characters"

        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords do not match"

        return errors
    
    def login_validator(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]

            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()): 
                errors['password'] = "Email/password combination invalid"
        else:
            errors["email"] = "User does not exist"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    
