from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    "用户"
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateTimeField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default='female',
                              verbose_name='性别')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮件地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name is None:
            return ''
        else:
            return self.name


class VerifyCode(models.Model):
    "邮箱验证码"
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    email = models.EmailField(max_length=64, verbose_name='邮件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
