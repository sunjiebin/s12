# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from Wolf.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)   #两次输入密码,调用了forms.PasswordInput工具来处理输入的密码
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name','is_active','is_admin')   #创建用户时必选的字段,可以自己添加

    def clean_password2(self):  #对输入的密码校验
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:  #如果pssword1和password2都存在,且不相等则报错
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):    #对输入的密码进行保存提交
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()      #对密码进行hash

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')        #创建用户时对哪些字段进行管理,似乎无效

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm       #修改用户用到
    add_form = UserCreationForm    #创建用户用到

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin','is_active')   # date_of_birth 改为了我们定义的name
    list_filter = ('is_admin','email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (       #创建用户的时候让你输入哪些字段
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)      #可以搜索的字段
    ordering = ('email',)           #排序字段
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(UserProfile, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)