from django.db import models

# Create your models here.

class Child(models.Model):
    child_name=models.CharField(max_length=100)
    child_age=models.IntegerField()
    location=models.CharField(max_length=100)
    child_image=models.ImageField(upload_to='child_image')