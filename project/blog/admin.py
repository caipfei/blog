from django.contrib import admin
from django import forms
from blog.models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# Register your models here.
#在这个文件中定制admin后台页面的显示

#重新定义创建用户的表单，继承自UserCreationForm
class MyUserCreationForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(MyUserCreationForm,self).__init__(*args,**kwargs)
        #在表单中加入新添加的两个字段
        self.fields['nick'] = forms.CharField(max_length=32,label="昵称")
        self.fields['email'] = forms.CharField(label="邮箱")
        #self.fields['email'].required = True
        #self.fields['nick'].required = True
        
#重新定义编辑用户的表单，继承自UserChangeForm    
class MyUserChangeForm(UserChangeForm):
    def __init__(self,*args,**kwargs):
        super(MyUserChangeForm,self).__init__(*args,**kwargs)
        #在表单中加入新字段
        self.fields['nick'] = forms.CharField(max_length=32,label="昵称")
        self.fields['email'] = forms.CharField(label="邮箱")
        #self.fields['email'].required = True
        #self.fields['nick'].required = True
        
class MyUserAdmin(UserAdmin):
    def __init__(self,*args,**kwargs):
        super(MyUserAdmin,self).__init__(*args,**kwargs)
        self.list_display = ('username','nick','email','is_active','is_staff','is_superuser')
        self.search_fields = ('username','nick','email')
        self.form = MyUserChangeForm   #设置用户表单为自定义表单
        self.add_form = MyUserCreationForm   #设置添加用户表单为自定义表单
        #以上属性都可以在django源码的UserAdmin类中找到，我们做了覆盖
    
    #这个方法的源码在admin/options.py文件的ModelAdmin这个类中，我们要重新定义它，已达到不同
    #权限的用户，返回的表单内容不同
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

#将新定义的模型注册        
admin.site.register(MyUser,MyUserAdmin)
























