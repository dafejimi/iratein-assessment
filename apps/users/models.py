# models.py
from django.db import models
from django.contrib.auth.models import User

class CustomUser(User):
    pass

class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')
    contact_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contact_users')


