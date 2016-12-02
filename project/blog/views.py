from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from .forms import RegisterForm,LoginForm,AvatarForm
#from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from blog.models import MyUser,Post,Comment,Follow
from django.template.context_processors import csrf
from json import loads
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.core.paginator import Paginator,InvalidPage
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
            user.follow(user)
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
            human = True
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
    followers = MyUser.objects.filter(fans__follower=request.user).all()
    paginator = Paginator(Post.objects.filter(author__in=followers).order_by('-timestamp').all(),20)
    page = request.GET.get('page',1)
    try:
        posts = paginator.page(page)
    except InvalidPage:
        posts = paginator.page(1)
    return render(request,'blog/home.html',{'posts':posts})
    
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
def postBlog(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag = request.POST.get('tag')
        abstract = request.POST.get('abstract')
        p = Post(title=title,genre=genre,content=content,tag=tag,abstract=abstract)
        p.author = request.user
        p.save()
        return HttpResponseRedirect(reverse('blog:home'))
    else:
        return render(request,'blog/post_blog.html')
        
def post(request,id):
    try:
        id = int(id)
    except:
        raise Http404()
    p = get_object_or_404(Post,id=id)
    comments = Comment.objects.filter(post=p).order_by('timestamp').all()
    user = p.author
    if not isinstance(request.user,AnonymousUser) and request.user.is_following(user):
        is_follow = 1
    else:
        is_follow = 0
    return render(request,'blog/post.html',{'post':p,'user':user,'comments':comments,'is_follow':is_follow})

def userInfo(request,id):
    try:
        id = int(id)
    except:
        raise Http404()
    user = get_object_or_404(MyUser,id=id)
    paginator = Paginator(Post.objects.filter(author=user),20)
    page = request.GET.get('page',1)
    try:
        posts = paginator.page(page)
    except InvalidPage:
        posts = paginator.page(1)
    if not isinstance(request.user,AnonymousUser) and request.user.is_following(user):
        is_follow = 1
    else:
        is_follow = 0
    return render(request,'blog/user.html',{'user':user,'posts':posts,'is_follow':is_follow})

@login_required
def comment(request):
    if request.method=='POST':
        body = request.POST.get('body')
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        comment = Comment(author=request.user,post=post,body=body)
        comment.save()
        return HttpResponseRedirect(reverse('blog:post',kwargs={'id':post_id}))
        
@login_required
def follow(request,id):
    try:
        id = int(id)
    except:
        raise Http404()
    user = get_object_or_404(MyUser,id=id)
    request.user.follow(user)
    old_url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(old_url)
        
@login_required
def unfollow(request,id):
    try:
        id = int(id)
    except:
        raise Http404()
    user = get_object_or_404(MyUser,id=id)
    request.user.unfollow(user)
    old_url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(old_url)
    
@login_required
def follows(request,id):
    try:
        id = int(id)
    except:
        raise Http404()
    user = get_object_or_404(MyUser,id=id)
    follow = user.guanzhu.all()
    if user == request.user:
        return render(request,'blog/myFollows.html',{'follow':follow})
    else:
        is_follow = 1 if request.user.is_following(user) else 0
        return render(request,'blog/follow.html',{'follow':follow,'user':user,'is_follow':is_follow})
        
@login_required
def fans(request,id):
    try:
        id = int(id)
    except:
        raise Http404()
    user = get_object_or_404(MyUser,id=id)
    fans = user.fans.all()
    if user == request.user:
        return render(request,'blog/myFans.html',{'fans':fans})
    else:
        is_follow = 1 if request.user.is_following(user) else 0
        return render(request,'blog/fans.html',{'fans':fans,'user':user,'is_follow':is_follow})
    
            

