from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    # Add other fields as needed

# Create your models here.
