from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from datetime import datetime
# Create your models here.

#集成AbstractUser类，实际上django的User也是继承这个类，我们要用自己的类替代django的User
class MyUser(AbstractUser):
    #增加两个新的属性
    nick = models.CharField(max_length=32,verbose_name="昵称")
    avatar = models.ImageField(upload_to='photo',null=True,blank=True,verbose_name="头像")
    
    def __str__(self):
        return self.username
        
    class Meta:
        verbose_name = '用户详情'
        verbose_name_plural = '用户详情'

class Post(models.Model):
    author = models.ForeignKey(MyUser,verbose_name="作者")
    title = models.CharField(max_length=100,verbose_name="标题")
    genre = models.IntegerField(verbose_name="类别")
    content = RichTextField('正文')
    tag = models.CharField(max_length=100,verbose_name="标签",blank=True,null=True)
    timestamp = models.DateTimeField(verbose_name='发表时间',default=datetime.now)
    abstract = models.TextField(verbose_name='摘要',max_length=255)
    
    class Meta:
        verbose_name = '博客列表'
        verbose_name_plural = '博客列表'
    def __str__(self):
        return self.title







    