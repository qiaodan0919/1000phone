from django.db import models

# Create your models here.
class User(models.Model):
    u_name = models.CharField(max_length=16,unique=True,null=False)
    u_passwd = models.CharField(max_length=16)
    u_email = models.CharField(max_length=16)
    u_file = models.ImageField(upload_to='%Y/%m/%d/')


class Movies(models.Model):
    postid = models.CharField(max_length=16, unique=True, null=False)
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    like_num = models.CharField(max_length=16)
    request_url = models.CharField(max_length=255)

class Swiper(models.Model):
    image = models.CharField(max_length=255)