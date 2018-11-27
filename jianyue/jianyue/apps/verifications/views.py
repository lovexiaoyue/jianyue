from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView
from django_redis import get_redis_connection
from jianyue.utils.captcha.captcha import captcha
from django.http import HttpResponse
from jianyue.libs import constants
from rest_framework import status
from rest_framework.response import Response
from jianyue.libs.yuntongxun.sms import CCP
from users.models import User
import random
from . import serializers
import logging
logger = logging.getLogger('loggers')

class ImageCodeView(APIView):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        """
        获取图片验证码
        """

        # 生成验证码图片
        text, image = captcha.generate_captcha()
        print(text)
        code_id = image_code_id
        print(code_id)
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return HttpResponse(image, content_type="images/jpg")


class SMSCodeView(GenericAPIView):
    """
    短信验证码
    """
    serializer_class = serializers.ImageCodeCheckSerializer

    def get(self, request, mobile):

        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = "%04d" % random.randint(0,999999)
        print(sms_code)
        # 保存验证码记录
        redis_conn = get_redis_connection("verify_codes")
        pl = redis_conn.pipeline()
        pl.multi()
        pl.setex("sms_%s" %mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" %mobile, constants.SMS_SEND_FLAG_REDIS_EXPIRES, 1)
        pl.execute()
        # 发送短信
        try:
            ccp = CCP()
            result = ccp.send_template_sms(mobile, [sms_code, 5], 1)
            if result == 0:
                return Response({"message":"success"},status.HTTP_200_OK)
            if result == -1:
                return Response({"message":"fall"}, status.HTTP_200_OK)
            else:
                return Response({"message":"error"}, status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            logger.error(e)
            return Response({"message": "error"}, status.HTTP_501_NOT_IMPLEMENTED)


class UserCountView(APIView):
    """
    查询用户名数量
    """

    def get(self, request, username):
        """
        查询指定名称用户
        """
        count = User.objects.filter(username=username).count()
        data = {
            "username":username,
            "count":count
        }
        return Response(data)


class MobileCountView(APIView):
    """
    查询手机号数量
    """

    def get(self, request, mobile):
        """
        查询指定手机号
        """

        count = User.objects.filter(mobile=mobile).count()
        data = {
            "mobile":mobile,
            "count":count
        }
        return Response(data)


