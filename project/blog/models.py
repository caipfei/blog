from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    nick = models.CharField(max_length=32,verbose_name="昵称")
    avatar = models.ImageField(upload_to='photo',null=True,blank=True,verbose_name="头像")
    
    class Meta:
        verbose_name = '用户详情'
        verbose_name_plural = '用户详情'

