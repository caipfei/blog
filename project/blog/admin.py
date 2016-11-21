from django.contrib import admin
from django import forms
from blog.models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# Register your models here.

class MyUserCreationForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(MyUserCreationForm,self).__init__(*args,**kwargs)
        self.fields['nick'] = forms.CharField(max_length=32,label="昵称")
        self.fields['email'] = forms.CharField(label="邮箱")
        self.fields['email'].required = True
        self.fields['nick'].required = True
        
    
class MyUserChangeForm(UserChangeForm):
    def __init__(self,*args,**kwargs):
        super(MyUserChangeForm,self).__init__(*args,**kwargs)
        self.fields['nick'] = forms.CharField(max_length=32,label="昵称")
        self.fields['email'] = forms.CharField(label="邮箱")
        self.fields['email'].required = True
        self.fields['nick'].required = True
        
    
#@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    def __init__(self,*args,**kwargs):
        super(MyUserAdmin,self).__init__(*args,**kwargs)
        self.list_display = ('username','nick','email','is_active','is_staff','is_superuser')
        self.search_fields = ('username','nick','email')
        self.form = MyUserChangeForm   #设置用户表单为自定义表单
        self.add_form = MyUserCreationForm   #设置添加用户表单为自定义表单
    def changelist_view(self,request,extra_context=None):
        if not request.user.is_superuser:
            self.fieldsets = ((None,{'fields':('username','password',)}),
                              (_('Personal info'),{'fields':('nick','email','avatar')}),
                              (_('Permissions'),{'fields':('is_active','is_staff','groups','user_permissions')}),
                              (_('Important dates'),{'fields':('last_login','date_joined')}),
                             )
            self.add_fieldsets = ((None,{'classes':('wide',),'fields':('username','nick',
            'password1','password2','email','is_active','is_staff','groups'),}),)
        else:
            self.fieldsets = ((None,{'fields':('username','password',)}),
                             (_('Personal info'),{'fields':('nick','email','avatar')}),
                             (_('Permissions'),{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
                             (_('Important dates'),{'fields':('last_login','date_joined')}),
            )
            self.add_fieldsets = ((_('用户信息'),{'classes':('wide',),'fields':('username','nick','password1','password2',
                                  'email','is_active','is_staff','is_superuser','groups','user_permissions'),}),)
        return super(MyUserAdmin,self).changelist_view(request,extra_context)
        
admin.site.register(MyUser,MyUserAdmin)
























