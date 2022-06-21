from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from djangoProject.settings import REGEX_EMAIL
from users.models import VerifyCode

User = get_user_model()

class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    def validate_email(self,email):
        """
        验证email
        :param data:
        :return:
        """
        # email是否注册
        if User.objects.filter(email = email).count():
            raise serializers.ValidationError('用户存在')
            # 验证邮箱号码合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError('邮箱格式错误')
            # 验证码发送频率
        one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_age, email=email).count():
            raise serializers.ValidationError('请一分钟后再次发送')
        return email

