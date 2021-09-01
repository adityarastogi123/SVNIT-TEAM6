from django.db import models

# Create your models here.
class History(models.Model):
    user=models.CharField(max_length=200,default='adide')
    history=models.CharField(max_length=500)
    def __str__(self):
        return self.history