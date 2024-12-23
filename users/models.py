from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
import hmac
import hashlib

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  # This will use our customized password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_password(self, raw_password):
        """Override set_password to use HMAC + Salt"""
        salt = os.urandom(16).hex()  # Generate a random Salt
        hashed_password = hmac.new(salt.encode(), raw_password.encode(), hashlib.sha256).hexdigest()
        self.password = f'{salt}${hashed_password}'  # Save salt and hash in the format: salt$hashed_password
