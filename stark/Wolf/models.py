#!/usr/bin/env python3
# Auther: sunjb

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):  #创建用户
        """
        Creates and saves a User with the given email, name
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password) #hash变成md5值
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):  #创建管理员
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#类名被修改成了UserProfile
class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)   #这里被修改成了自定义的name
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    token = models.CharField(max_length=16,default='abc')
    objects = MyUserManager()

    USERNAME_FIELD = 'email'    #校验时验证的字段,这里的email就是登录用户名
    REQUIRED_FIELDS = ['name']  #必填字段,这里修改成了name,我们定义为用户名称

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):     #自定义权限系统
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):  #对模块的权限
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property   #属性方法
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin