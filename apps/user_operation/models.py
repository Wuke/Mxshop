from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from goods.models import Goods
# Create your models here.

User = get_user_model()


class UserFav(models.Model):

    "用户收藏"

    user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,verbose_name='商品',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name='用户收藏'
        verbose_name_plural=verbose_name
        unique_together = ('user','goods')


    def __str__(self):
        return self.user.username

class UserLeavingMessage(models.Model):

    "用户留言"

    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '查询'),
        (4, '售后'),
        (5, '求购'),
    )

    user = models.ForeignKey(User, verbose_name='用户',on_delete=models.CASCADE)
    msg_type = models.IntegerField(default=1,choices=MESSAGE_CHOICES,verbose_name='留言类型',
                                   help_text='留言类型：1：留言，2：投诉，3：查询，4：售后，5：求购')
    subject = models.CharField(max_length=100,default='',verbose_name='主题')
    message = models.TextField(default='',verbose_name='留言内容',help_text='留言内容')
    file = models.FileField(upload_to='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject

class UserAddress(models.Model):

    "用户收货地址"

    user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    district = models.CharField(max_length=100, default='', verbose_name='区')
    address = models.CharField(max_length=100,default='',verbose_name='详细地址')
    signer_name = models.CharField(max_length=100,default='',verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11,default='',verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = '用户收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
