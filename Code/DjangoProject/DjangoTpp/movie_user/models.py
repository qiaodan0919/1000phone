from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
from movie_user.model_constant import PERMISSION_NONE

COMMON_USER = 0
BLACK_USER = 1
VIP_USER = 2


class MovieUser(models.Model):
    username = models.CharField(max_length=32, unique=True)
    _password = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, unique=True)
    is_delete = models.BooleanField(default=False)
    permission = models.IntegerField(default=PERMISSION_NONE)

    @property
    def password(self):
        # raise Exception("can't access")
        return self._password

    @password.setter
    def password(self, password_value):
        self._password = make_password(password_value)

    def check_pass(self, password_value):
        print(self._password)

        return check_password(password_value, self._password)

    def check_permission(self, permission):
        if BLACK_USER & self.permission == BLACK_USER:
            return False
        else:
            return permission & self.permission == permission
