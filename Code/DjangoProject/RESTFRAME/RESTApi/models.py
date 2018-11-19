from django.db import models

# Create your models here.

class UserModel(models.Model):
    u_name = models.CharField(max_length=32)
    u_password = models.CharField(max_length=256)

    is_super = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)