#from django.db import models
from djongo import models
# Create your models here.
class Diseases(models.Model):
    sintomas = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
