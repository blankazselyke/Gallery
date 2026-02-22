from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Photo(models.Model):
    title = models.CharField(max_length=40) 
    image = models.ImageField(upload_to='photos/')
    upload_date = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title