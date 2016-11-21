#coding:utf-8

from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^register/$',views.register,name="register"),
    url(r'^login/$',views.login_view,name="login"),
    url(r'^logout/$',views.logout_view,name="logout"),
    url(r'^check_user/$',views.check_username,name="check_user"),
    url(r'^test/$',views.test),
    url(r'^home/$',views.home,name="home")
]