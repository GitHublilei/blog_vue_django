import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator
from blog_vue_django.settings import REGEX_MOBILE
from datetime import datetime, timedelta
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    sms
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否已注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')
        # 验证发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送超过60s')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    serializer
    """
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4)
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')])
    password = serializers.CharField(required=True, style={'input_type': 'password'}, label="密码", write_only=True)

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("add_time")
        if verify_records:
            last_record = verify_records[0]

            five_minutes_age = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_age > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        # fields = ("username", "mobile", "password")
        fields = ("username", "code", "mobile", "password")
