from django.db import models

# Create your models here.

class Students(models.Model):
    s_name = models.CharField(max_length=32)
    s_age = models.IntegerField(default=1)