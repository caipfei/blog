from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .forms import RegisterForm,LoginForm,AvatarForm
#from django.contrib.auth.models import User
from blog.models import MyUser
from django.template.context_processors import csrf
from json import loads
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            nick = data['nick']
            password = data['password1']
            email = data['email']
            user = MyUser.objects.create_user(username=username,nick=nick,email=email)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.info(request,'注册成功，请登录')
            return HttpResponseRedirect(reverse('blog:login'))
        else:
            # messages.info(request,'注册失败')
            # return HttpResponseRedirect(reverse('blog:register'))
            c = {'form':form}
            c.update(csrf(request))
            return render(request,'blog/register.html',c)
    else:
        form = RegisterForm()
    c = {'form':form}
    c.update(csrf(request))
    return render(request,'blog/register.html',c)

def check_username(request):
    if request.method == 'POST':
        data = loads(request.body.decode('utf-8'))
        username = data.get('username','')
        user = MyUser.objects.filter(username=username).all()
        if user:
            return JsonResponse({'user_exist':'exist'})
        else:
            return JsonResponse({'user_exist':'not_exist'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username','')
            password = data.get('password','')
            remember = data.get('remember_me')
            user = authenticate(username=username,password=password)
            if user and user.is_active:
                login(request,user)
                if remember == False:  
                    request.session.set_expiry(0)
                #如果请求中有next参数，则返回到next页面，否则返回到index页面
                if request.GET.get('next'):  
                    redirecturl = request.GET['next']
                    return HttpResponseRedirect(redirecturl)
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request,'用户名或密码错误')
                return HttpResponseRedirect(reverse('blog:login'))
    else:
        form = LoginForm()
    c = {'form':form}
    c.update(csrf(request))
    return render(request,'blog/login.html',c)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:login'))
    
@login_required
def test(request):
    return HttpResponse('this is a secret page')
    
@login_required
def home(request):
    return render(request,'blog/home.html')
    
@login_required
def avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST,request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data.get('avatar')
            user = request.user
            if user.avatar:
                path = user.avatar.path
                os.remove(path)
            user.avatar = avatar
            user.save()
            return HttpResponseRedirect(reverse('blog:home'))
    else:
        form = AvatarForm()
    c = {'form':form}
    c.update(csrf(request))
    return render(request,'blog/avatar.html',c)

@login_required
def info(request):
    return render(request,'blog/info.html')

@login_required
def post_blog(request):
    return render(request,'blog/post_blog.html')








    
            

