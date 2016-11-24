#coding:utf-8

from django import forms
#from django.contrib.auth.models import User
from blog.models import MyUser
from django.contrib.auth.password_validation import validate_password
import re
from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名",min_length=3,max_length=150,
        widget=forms.TextInput(attrs={'id':'username','class':'form_field','placeholder':'至少3位字符'}),
        error_messages={'required':'用户名不能为空','min_length':'用户名最少为3位字符'})
    nick = forms.CharField(label="昵称",min_length=3,max_length=32,widget=forms.TextInput(attrs={'id':'nick',
        'class':'form_field','placeholder':'至少3位字符'}))
    password1 = forms.CharField(label='密码',min_length=6,widget=forms.PasswordInput(attrs={'id':
        'password1','class':'form_field','placeholder':'至少6位字符'}),error_messages={'required':'密码不能为空',
        'min_length':'密码最小长度为6位'})
    password2 = forms.CharField(label="确认密码",widget=forms.PasswordInput(attrs={'id':'password2',
        'class':'form_field'}),error_messages={'required':'字段不能为空'})
    email = forms.EmailField(label="邮箱",widget=forms.EmailInput(attrs={'id':'email',
        'class':'form_field'}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = MyUser.objects.filter(username=username).all()
        if user:
            raise forms.ValidationError('该用户名已存在')
        return username
    
    def clean_password2(self):
        passwd1 = self.cleaned_data.get('password1')
        passwd2 = self.cleaned_data.get('password2')
        if passwd1 and passwd2 and passwd1 != passwd2:
            raise forms.ValidationError('两次输入的密码不一致')
        return passwd2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        r = re.compile(r'[\w_]+@\w+(\.\w+)+')
        if not r.match(email):
            raise forms.ValidationError('邮箱格式不正确')
        return email
    
    def clean_nick(self):
        nick = self.cleaned_data.get('nick')
        user = MyUser.objects.filter(nick=nick).all()
        if user:
            raise forms.ValidationError('该昵称已被使用')
        return nick
    
class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",widget=forms.TextInput(attrs={'class':'input',
        'autofocus':'autofocus'}))
    password = forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'class':'input'}))
    remember_me = forms.BooleanField(label="记住密码",initial=False,required=False,
        widget=forms.CheckboxInput(attrs={'class':'input'}))

class AvatarForm(forms.Form):
    avatar = forms.ImageField(label="头像")














    