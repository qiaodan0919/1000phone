from django.db import models

# Create your models here.

class UserModel(models.Model):
    u_name = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)

    is_super = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.u_name

class AddressModel(models.Model):
    a_address = models.CharField(max_length=256)
    a_user = models.ForeignKey(UserModel, related_name='address_list', null=True, blank=True)

    def __str__(self):
        return self.a_address