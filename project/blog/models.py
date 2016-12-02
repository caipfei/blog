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
        
    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            f.save()
    def unfollow(self,user):
        Follow.objects.filter(follower=self).filter(followed=user).all().delete()
    def is_following(self,user):
        return self.guanzhu.filter(followed=user).first()
    def is_followed_by(self,user):
        return self.fans.filter(follower=user).first()
    def followed_list(self):
        followeds = self.guanzhu.all()
        fl = []
        for f in followeds:
            fl.append(f.followed)
        return fl
    
    @staticmethod
    def follow_self():
        for user in MyUser.objects.all():
            user.follow(user)
            
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

class Comment(models.Model):
    author = models.ForeignKey(MyUser,verbose_name='评论者')
    post = models.ForeignKey(Post,verbose_name='文章')
    body = models.TextField(verbose_name="内容")
    timestamp = models.DateTimeField(default=datetime.now,verbose_name="发表时间")
    disabled = models.BooleanField(default=False,verbose_name="是否禁用")
    
class Follow(models.Model):
    follower = models.ForeignKey(MyUser,verbose_name='关注者',related_name="guanzhu")
    followed = models.ForeignKey(MyUser,verbose_name='被关注者',related_name='fans')
    timestamp = models.DateTimeField(default=datetime.now,verbose_name='关注时间')
















    