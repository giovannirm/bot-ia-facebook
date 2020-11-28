#from django.db import models
from djongo import models

class Diseases(models.Model):
    race = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    symptom = models.JSONField()    
    answer = models.CharField(max_length=500)
    class Meta:        
        db_table = 'diseases'