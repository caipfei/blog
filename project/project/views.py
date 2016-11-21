#coding:utf-8
from django.shortcuts import render_to_response,render
from django.template import RequestContext

def index(request):
    # info = list(request.META.items())
    # info = sorted(info)
    return render(request,'index.html')

