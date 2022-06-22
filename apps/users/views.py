from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from djangoProject import settings
from .models import VerifyCode
from .serializer import EmailSerializer,UserRegSerializer
from django.core.mail import EmailMessage
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler

User = get_user_model()

#encoding=utf-8


class SendVerifyCode(object):
    @staticmethod
    def send_email_code(code,email):
        email = EmailMessage(
        subject='验证码',
        body=code,
        from_email=settings.EMAIL_HOST_USER,
        to=[email]
        )
        email.fail_silently=False
        email.send()

# def get_user_by_account(account):
#     """
#     根据帐号获取user对象
#     :param account: 账号，可以是用户名username，也可以是手机号mobile, 或者其他的数据
#     :return: User对象 或者 None
#     """
#     try:
#         user = User.objects.filter(Q(username=account) | Q(email=account)).first()
#     except User.DoesNotExist:
#         return None
#     else:
#         return user

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self,request, username=None,password=None,**kwargs):
        try:
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        except User.DoesNotExist:
            return None
        else:
            return user

class EmailCodeViewset(CreateModelMixin,viewsets.GenericViewSet):

    serializer_class = EmailSerializer

    def generate_code(self):
        """
        生成6位数验证码 防止破解
        :return:
        """
        seeds = "1234567890abcdefghijklmnopqrstuvwxyz"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        # 自定义的 create() 的内容
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 这一步相当于发送前验证
        # 从 validated_data 中获取 mobile
        email = serializer.validated_data["email"]
        # 随机生成code
        code = self.generate_code()
        # 发送短信或邮件验证码
        sms_status = SendVerifyCode.send_email_code(code=code, email=email)
        if sms_status == 0:
            # 记录日志
            return Response({"msg": "邮件发送失败"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, email=email)
            # 保存验证码
            code_record.save()
            return Response(
                {"msg": f"验证码已经向 {email} 发送完成"}, status=status.HTTP_201_CREATED
            )

class UserViewset(CreateModelMixin,viewsets.GenericViewSet):

    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()