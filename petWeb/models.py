#from django.db import models
from djongo import models
# Create your models here.
class Posts(models.Model):
    task = models.CharField(max_length=30)
    description = models.CharField(max_length=100)