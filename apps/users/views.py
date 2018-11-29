from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice

from .serializers import UserRegSerializer, SmsSerializer
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成4位数字的验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        sms = self.generate_code()

        code_record = VerifyCode(code=sms, mobile=mobile)
        code_record.save()

        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"mobile": mobile, "sms": sms}, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    创建用户
    """
    serializer_class = UserRegSerializer
