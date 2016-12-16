from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self, form):
        errors = []
        if len(form['first_name']) == 0:
            errors.append("First name required")
        elif len(form['first_name']) < 2:
            errors.append("First name must be at least 2 characters")
        elif not form['first_name'].isalpha():
            errors.append("First name must only consist of letters")
        if len(form['last_name']) == 0:
            errors.append("Last name required")
        elif len(form['last_name']) < 2:
            errors.append("Last name must be at least 2 characters")
        elif not form['last_name'].isalpha():
            errors.append("Last name must only consist of letters")
        if len(form['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form['email']):
            errors.append("Please enter a valid email")
        elif User.objects.filter(email=form['email']):
            errors.append("Account already exist for that email")
        if len(form['password']) == 0:
            errors.append("Password required")
        elif len(form['password']) <8:
            errors.append("Password must be at least 8 characters")
        if len(form['passconf']) == 0:
            errors.append("Password confirmation required")
        elif (form['passconf'] != form['password']):
            errors.append("Password doesnt match confirmation")

        return errors
    def register(self, form):
        hashed_pass = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        return self.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=hashed_pass)

    def check_login(self, form):
        #first we find if we have a user in DB with that email:
        check_user = self.filter(email=form['email'])
        #***NEED TO VALIDATE INPUTS**** from above

        if check_user:
            user = check_user[0]
            #if that is true then we check the password:
            if bcrypt.hashpw(form['password'].encode(), user.password.encode()) == user.password:
                #if those match, then we add to session, and that's a login
                return user
        #else any other case, its a bad login
        return None

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
