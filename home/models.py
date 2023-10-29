from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Child(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    child_name=models.CharField(max_length=100)
    child_age=models.IntegerField()
    location=models.CharField(max_length=100)
    child_image=models.ImageField(upload_to='child_image')
    birth_mark=models.CharField(max_length=100,default="none")
    child_height=models.IntegerField(default=None)
    
class Lostchild(models.Model):
    child_name=models.CharField(max_length=100)
    child_age=models.IntegerField()
    state=models.CharField(max_length=100)
    fir_no=models.CharField(max_length=100)
    description=models.CharField(max_length=100,default=None)
    child_image=models.ImageField(upload_to='child_image')
    birth_mark=models.CharField(max_length=100,default="none")
    child_height=models.IntegerField(default=None)

