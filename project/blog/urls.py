#coding:utf-8

from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^register/$',views.register,name="register"),
    url(r'^login/$',views.login_view,name="login"),
    url(r'^logout/$',views.logout_view,name="logout"),
    url(r'^check_user/$',views.check_username,name="check_user"),
    url(r'^test/$',views.test),
    url(r'^home/$',views.home,name="home"),
    url(r'^avatar/$',views.avatar,name="avatar"),
    url(r'^info/$',views.info,name='info'),
    url(r'^postBlog/$',views.postBlog,name="postBlog"),
    url(r'^posts/(?P<id>\d+)/$',views.post,name="post"),
    url(r'^user/(?P<id>\d+)/$',views.userInfo,name='userInfo'),
    url(r'^comment/$',views.comment,name='comment'),
    url(r'^follow/(?P<id>\d+)/$',views.follow,name="follow"),
    url(r'^unfollow/(?P<id>\d+)/$',views.unfollow,name="unfollow"),
    url(r'^user/(?P<id>\d+)/follows/$',views.follows,name="follows"),
    url(r'^user/(?P<id>\d+)/fans/$',views.fans,name='fans'),
]