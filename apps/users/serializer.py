from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from rest_framework.validators import UniqueValidator
from djangoProject.settings import REGEX_EMAIL
from users.models import VerifyCode

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, label='邮箱地址')

    def validate_email(self, email):
        """
        验证email
        :param email:
        :param data:
        :return:
        """
        # email是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError('用户存在')
            # 验证邮箱号码合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError('邮箱格式错误')
            # 验证码发送频率
        one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_age, email=email).count():
            raise serializers.ValidationError('请一分钟后再次发送')
        return email


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=6, min_length=6, write_only=True, required=True, help_text='验证码',
                                 label='验证码',
                                 error_messages={
                                     'required': '请输入验证码',
                                     'max_length': "验证码格式错误",
                                     'min_length': "验证码格式错误",
                                     'blank': '请输入验证码'
                                 })
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户存在")])
    password = serializers.CharField(style={'input_type': 'password'}, label='密码', write_only=True)

    def validate_code(self, code):
        verify_record = VerifyCode.objects.filter(email=self.initial_data['username']).order_by('-add_time')
        if verify_record:
            last_record = verify_record[0]
            two_minute_age = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
            if two_minute_age > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
            return code
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs['email'] = attrs['username']
        del attrs['code']
        # self.fields.pop('code')
        return attrs

    # 在serialiazer中对密码加密
    # def create(self, validated_data):
    #     user = super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    class Meta:
        model = User
        fields = ('username', 'email', 'code', 'password')
