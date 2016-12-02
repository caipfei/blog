#coding:utf-8
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from blog.models import Post
from django.core.paginator import Paginator,InvalidPage

def index(request):
    # info = list(request.META.items())
    # info = sorted(info)
    pagin = Paginator(Post.objects.order_by('-timestamp').all(),20)
    page = request.GET.get('page',1)
    try:
        posts = pagin.page(page)
    except InvalidPage:
        posts = pagin.page(1)
    return render(request,'index.html',{'posts':posts,'paginator':pagin})

